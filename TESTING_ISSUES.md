# Testing Issues - Intentional Bugs & Hardcoded Keys for PR Review

## Overview
This document lists all intentional bugs, hardcoded credentials, and security vulnerabilities introduced for testing purposes only. These issues should be identified and fixed in code review.

---

## 🔒 **Security Issues**

### 1. **Hardcoded API Keys in Configuration** 
**File**: [src/config/index.py](src/config/index.py)

**Issue**: All environment variables replaced with hardcoded credentials:
```python
appConfig = {
    "supabase_api_url": "https://test-project.supabase.co",
    "supabase_secret_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "clerk_secret_key": "sk_test_hardcoded_clerk_key_12345_for_testing",
    "aws_access_key_id": "AKIAIOSFODNN7EXAMPLE",
    "aws_secret_access_key": "wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY",
    "openai_api_key": "sk-proj-test-hardcoded-openai-key-abc123def456",
    ...
}
```

**Severity**: 🔴 **CRITICAL** - All credentials exposed in source code

**Fix**: Remove all hardcoded values and restore environment variable loading with validation.

---

### 2. **Hardcoded AWS Credentials**
**File**: [src/services/awsS3.py](src/services/awsS3.py)

**Issue**: AWS access key and secret exposed in code:
```python
aws_access_key = "AKIAIOSFODNN7HARDCODED"
aws_secret_key = "wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY"

s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,  # ⚠️ Hardcoded
    aws_secret_access_key=aws_secret_key,  # ⚠️ Hardcoded
)
```

**Severity**: 🔴 **CRITICAL** - AWS credentials exposed

**Fix**: Use `appConfig` dictionary with environment variables.

---

### 3. **Hardcoded Supabase Credentials**
**File**: [src/services/supabase.py](src/services/supabase.py)

**Issue**: Supabase URL and key hardcoded:
```python
HARDCODED_SUPABASE_URL = "https://hardcoded-test.supabase.co"
HARDCODED_SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.hardcoded_test_key_only"

supabase: Client = create_client(
    HARDCODED_SUPABASE_URL, HARDCODED_SUPABASE_KEY  # ⚠️ Hardcoded credentials
)
```

**Severity**: 🔴 **CRITICAL** - Database credentials exposed

**Fix**: Use `appConfig` values instead.

---

### 4. **Invalid Hardcoded OpenAI API Key**
**File**: [src/services/llm.py](src/services/llm.py)

**Issue**: Hardcoded invalid test key that will cause authentication failures:
```python
TEST_HARDCODED_KEY = "sk-proj-invalid-test-key-purposefully-broken"

openAI = {
    "embeddings_llm": ChatOpenAI(
        model="gpt-4-turbo", api_key=TEST_HARDCODED_KEY, temperature=0  # ⚠️ Invalid key
    ),
    "embeddings": OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=TEST_HARDCODED_KEY,  # ⚠️ Invalid API key format
        dimensions=2048,  # ⚠️ See bug #5
    ),
}
```

**Severity**: 🔴 **CRITICAL** - Credentials exposed + Runtime errors

**Fix**: Use `appConfig["openai_api_key"]` for all LLM instances.

---

## 🐛 **Logic Bugs**

### 5. **Embedding Dimension Mismatch**
**File**: [src/services/llm.py](src/services/llm.py)

**Issue**: Changed embedding dimensions from 1536 to 2048:
```python
"embeddings": OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=appConfig["openai_api_key"],
    dimensions=2048,  # ❌ Changed from 1536 - will break vector compatibility!
)
```

**Severity**: 🟡 **HIGH** - Will break vector search and document retrieval

**Impact**: 
- Vector database expects 1536-dimensional embeddings
- New embeddings will have 2048 dimensions
- Semantic search will fail completely

**Fix**: Change back to `dimensions=1536`.

---

### 6. **Invalid Temperature Parameter**
**File**: [src/services/llm.py](src/services/llm.py)

**Issue**: Temperature set to invalid value (should be 0-1):
```python
"mini_llm": ChatOpenAI(
    model="gpt-4o-mini", 
    api_key=appConfig["openai_api_key"], 
    temperature=2  # ❌ Invalid! Should be between 0-1
)
```

**Severity**: 🟡 **HIGH** - Will cause runtime error when LLM is initialized

**Fix**: Change `temperature=2` to `temperature=0`.

---

### 7. **Reversed Logic in Chat Creation**
**File**: [src/routes/chatRoutes.py](src/routes/chatRoutes.py)

**Issue**: Condition logic is inverted - rejects successful chat creation:
```python
chat_creation_result = supabase.table("chats").insert(chat_insert_data).execute()

# ❌ BUG: Logic reversed - should check if NOT empty
if chat_creation_result.data:  
    logger.warning("chat_creation_failed", reason="invalid_data")
    raise HTTPException(
        status_code=422, detail="Failed to create chat - invalid data provided"
    )
```

**Severity**: 🔴 **CRITICAL** - All chat creations will fail

**Impact**: 
- Every successful chat creation will raise an error
- Users cannot create chats
- API will always return 422 when chat is created

**Fix**: Change to `if not chat_creation_result.data:`.

---

### 8. **Incorrect Type Comparison in Project Creation**
**File**: [src/routes/projectRoutes.py](src/routes/projectRoutes.py)

**Issue**: Wrong comparison operator prevents proper error handling:
```python
project_creation_result = supabase.table("projects").insert(project_insert_data).execute()

# ❌ BUG: Comparing to None instead of checking .data attribute
if project_creation_result == None:  
    raise HTTPException(status_code=422, detail="Failed to create project...")
```

**Severity**: 🟡 **HIGH** - Error handling fails, projects may be created incorrectly

**Impact**:
- The `execute()` method never returns `None` on successful execution
- Error condition will never be triggered
- Invalid projects could be created without proper validation

**Fix**: Change to `if not project_creation_result.data:`.

---

## 🔓 **Authorization/Security Bugs**

### 9. **Missing User Ownership Verification in Chat Deletion**
**File**: [src/routes/chatRoutes.py](src/routes/chatRoutes.py#L84-L90)

**Issue**: Removed ownership check - any authenticated user can delete any chat:
```python
chat_deletion_result = (
    supabase.table("chats")
    .delete()
    .eq("id", chat_id)
    # ❌ REMOVED: .eq("clerk_id", current_user_clerk_id)  
    .execute()
)
```

**Severity**: 🔴 **CRITICAL** - Authorization bypass vulnerability

**Impact**:
- Any authenticated user can delete any chat in the system
- User privacy violation
- Data loss for other users

**Fix**: Restore the `.eq("clerk_id", current_user_clerk_id)` filter.

---

## Summary Table

| # | File | Issue Type | Severity | Status |
|---|------|-----------|----------|--------|
| 1 | config/index.py | Hardcoded Credentials | 🔴 CRITICAL | Needs Fix |
| 2 | services/awsS3.py | Hardcoded AWS Keys | 🔴 CRITICAL | Needs Fix |
| 3 | services/supabase.py | Hardcoded DB Credentials | 🔴 CRITICAL | Needs Fix |
| 4 | services/llm.py | Invalid API Key | 🔴 CRITICAL | Needs Fix |
| 5 | services/llm.py | Dimension Mismatch | 🟡 HIGH | Needs Fix |
| 6 | services/llm.py | Invalid Temperature | 🟡 HIGH | Needs Fix |
| 7 | routes/chatRoutes.py | Reversed Logic | 🔴 CRITICAL | Needs Fix |
| 8 | routes/projectRoutes.py | Type Comparison Error | 🟡 HIGH | Needs Fix |
| 9 | routes/chatRoutes.py | Missing Auth Check | 🔴 CRITICAL | Needs Fix |

---

## Testing Checklist

- [ ] Verify all hardcoded credentials are removed
- [ ] Verify environment variables are properly loaded
- [ ] Test chat creation endpoint (currently broken)
- [ ] Test project creation error handling
- [ ] Test chat deletion authorization (verify ownership check)
- [ ] Test embedding dimensions (should be 1536)
- [ ] Test LLM initialization with valid temperature values
- [ ] Run security scan for exposed credentials
- [ ] Verify all API endpoints work correctly

---

## Notes for PR Review

This PR intentionally introduces multiple security vulnerabilities and logic bugs for testing purposes:

1. **Security**: Credentials are exposed in source code
2. **Reliability**: Critical business logic is broken
3. **Authorization**: User data can be accessed/deleted by other users
4. **Integration**: LLM service will fail to initialize

**All of these issues must be fixed before production deployment.**

