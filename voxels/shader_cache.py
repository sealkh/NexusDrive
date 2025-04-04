import hashlib
import pickle
import os
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "shader_cache"

class ShaderCache:
    @staticmethod
    def get_cache_key(vertex_path, fragment_path):
        """Генерация ключа на основе содержимого файлов"""
        def file_hash(path):
            return hashlib.md5(Path(path).read_bytes()).hexdigest()
            
        return f"{file_hash(vertex_path)}_{file_hash(fragment_path)}.cache"

    @staticmethod
    def load(vertex_path, fragment_path): # Loading from cache
        if not CACHE_DIR.exists():
            os.makedirs(CACHE_DIR)

        cache_file = CACHE_DIR / ShaderCache.get_cache_key(vertex_path, fragment_path)
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        return None

    @staticmethod
    def save(vertex_path, fragment_path, program_binary): # Saving to cashe
        cache_file = CACHE_DIR / ShaderCache.get_cache_key(vertex_path, fragment_path)
        with open(cache_file, 'wb') as f:
            pickle.dump({
                'format': glGetProgramiv(program_binary, GL_PROGRAM_BINARY_FORMATS)[0],
                'binary': program_binary
            }, f)