"""Module with pwd_context defining the hash function used for storing passwords."""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""CryptContext defining the hash function for the passwords."""