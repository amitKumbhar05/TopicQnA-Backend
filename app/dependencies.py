import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Header, HTTPException, status
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    # 1. Check for Base64 Env Var (Production / Render)
    firebase_base64 = os.getenv("FIREBASE_CREDENTIALS_BASE64")
    
    if firebase_base64:
        try:
            # Decode the Base64 string back to a JSON dictionary
            decoded_json = base64.b64decode(firebase_base64).decode("utf-8")
            cred_dict = json.loads(decoded_json)
            cred = credentials.Certificate(cred_dict)
        except Exception as e:
            print(f"Error decoding Firebase credentials: {e}")
            raise e
    
    # 2. Fallback to File Path (Local Development)
    else:
        # This reads the path from .env (e.g., ./firebase-creds.json)
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not cred_path:
            raise ValueError("No Firebase credentials found (Base64 or File)")
        cred = credentials.Certificate(cred_path)

    firebase_admin.initialize_app(cred)


def get_current_user(authorization: str = Header(...)):
    """
    Validates Firebase Bearer Token.
    Returns the user's UID (string).
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid authentication scheme"
        )
    
    token = authorization.split("Bearer ")[1]
    
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        return uid
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid or expired token"
        )