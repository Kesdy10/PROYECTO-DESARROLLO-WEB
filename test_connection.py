#!/usr/bin/env python3
"""
Script para probar la conexión a la base de datos de Railway
"""
import os
import psycopg2
from urllib.parse import urlparse

def test_railway_connection():
    # Tu URL de Railway
    database_url = "postgresql://postgres:FvYWODdjiusyFFvUOBIOnDWTjbAOXQEV@centerbeam.proxy.rlwy.net:36876/railway"
    
    try:
        # Parsear la URL
        parsed = urlparse(database_url)
        
        print("🔍 Probando conexión a Railway PostgreSQL...")
        print(f"Host: {parsed.hostname}")
        print(f"Puerto: {parsed.port}")
        print(f"Base de datos: {parsed.path[1:]}")  # Quitar el '/' inicial
        print(f"Usuario: {parsed.username}")
        
        # Intentar conexión
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print("✅ Conexión exitosa!")
        print(f"Versión PostgreSQL: {version[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    test_railway_connection()