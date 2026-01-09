# JWT Token Fix - IMPORTANT

## Issue
The error "Subject must be a string" / "Not enough segments" was caused by JWT tokens being created with integer identities instead of strings.

## What Was Fixed
1. **auth.py** - Changed `create_access_token(identity=user.id)` to `create_access_token(identity=str(user.id))`
2. **All resources** - Added `int(get_jwt_identity())` to convert the string back to integer when querying users
3. **Added JWT error handlers** in app.py for better error messages

## CRITICAL: Users Must Re-Login

**All existing tokens are invalid!** Users must:

1. **Log out** from the frontend
2. **Log back in** to get a new token with the correct format
3. Old tokens will continue to fail with "Subject must be a string"

## Testing

Run the test script to verify:
```bash
python test_token.py
```

## For Frontend Users

If you see the error "Not enough segments" or "Subject must be a string":

1. Clear localStorage:
   ```javascript
   localStorage.removeItem('token');
   localStorage.removeItem('user');
   ```

2. Or just log out and log back in through the UI

3. Try creating a bakery again

The frontend will auto-logout after 5 seconds when it detects this JWT error, so you should be redirected to login automatically.
