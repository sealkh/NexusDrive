import os
import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from pathlib import Path

class VoxelEngineCore:
    def __init__(self, window_config, shader_config, voxel_config):
        # Инициализация GLFW
        if not glfw.init():
            raise RuntimeError("GLFW initialization failed")
        
        self.window = glfw.create_window(
            window_config['width'], window_config['height'],
            window_config['title'], None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Window creation failed")
        
        glfw.make_context_current(self.window)
        self._setup_callbacks()
        self._init_geometry()
        
        # Шейдеры
        self.shader_config = shader_config
        # self.uniforms_list = shader_config.UNIFORMS
        self.uniforms = {}
        self._load_shaders()

        
        # Воксели (опционально)
        # self._init_voxels()

    def _setup_callbacks(self):
        glfw.set_key_callback(self.window, self._key_callback)
        glfw.set_framebuffer_size_callback(self.window, self._resize_callback)

    def _init_geometry(self):
        vertices = np.array([-1, -1, 1, -1, -1, 1, 1, 1], dtype=np.float32)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        
    def _load_shaders(self):
        self.program = None
        try:
            # 1. Loading sources
            with open(self.shader_config['vertex'], 'r') as f:
                vs_src = f.read()
            with open(self.shader_config['fragment'], 'r') as f:
                fs_src = f.read()

            # 2. Compile
            vs = compileShader(vs_src, GL_VERTEX_SHADER)
            fs = compileShader(fs_src, GL_FRAGMENT_SHADER)
            new_program = compileProgram(vs, fs)

            # 3. Checking success
            if not glGetProgramiv(new_program, GL_LINK_STATUS):
                error = glGetProgramInfoLog(new_program).decode()
                raise RuntimeError(f"Shader link error: {error}")

            # 4. Setting new shader
            if self.program:
                glDeleteProgram(self.program)
            self.program = new_program
            glUseProgram(self.program)
            self._cache_uniforms()
            print("Шейдеры успешно перезагружены!")
            width, height = glfw.get_framebuffer_size(self.window)
            glUniform2f(self.uniforms["u_res"], width, height)
            return True

        except Exception as e:
            print(f"Ошибка перезагрузки шейдеров: {str(e)}")
            if 'new_program' in locals():
                glDeleteProgram(new_program)
            return False

    def _cache_uniforms(self):
        self.uniforms = {}
        glUseProgram(self.program)
        for name in self.shader_config['uniforms']:
            loc = glGetUniformLocation(self.program, name)
            if loc == -1:
                print(f"Предупреждение: uniform '{name}' не найден")
            self.uniforms[name] = loc

    def _key_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        elif key == glfw.KEY_R and action == glfw.PRESS:
            self._load_shaders()

    def _resize_callback(self, window, width, height):
        glViewport(0, 0, width, height)
        if "u_res" in self.uniforms and self.uniforms["u_res"] != -1:
            glUseProgram(self.program)
            glUniform2f(self.uniforms["u_res"], width, height)

    def run(self):
        while not glfw.window_should_close(self.window):
            self._render_frame()
            glfw.poll_events()
        
        glfw.terminate()

    def _render_frame(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(self.program)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glfw.swap_buffers(self.window)