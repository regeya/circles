import moderngl
import numpy as np

VERTEX_SHADER = """
#version 330
in vec2 in_vert;
in vec2 in_uv;
out vec2 v_uv;

void main() {
    v_uv = in_uv;
    gl_Position = vec4(in_vert, 0.0, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 330
uniform sampler2D tex;
uniform sampler2D paletteTex;
uniform vec4 SourceSize;
uniform vec4 OutputSize;
in vec2 v_uv;
out vec4 f_color;

#define SCANLINE_WEIGHT 1.2
#define SCANLINE_GAP_BRIGHTNESS 0.65
#define BLOOM_FACTOR 1.25
#define INPUT_GAMMA 2.2
#define OUTPUT_GAMMA 2.2
#define BLUR_OFFSET 0.75 

void main() {
    vec2 uv = v_uv;

    // 1. Curvature
    // 1. Curvature (Keep this unchanged)
    vec2 cc = uv - 0.5;
    float dist = dot(cc, cc) * 0.002;
    uv = (cc + cc * dist) + 0.5;

    if (uv.x < 0.0 || uv.y < 0.0 || uv.x > 1.0 || uv.y > 1.0) {
        f_color = vec4(0.0, 0.0, 0.0, 1.0);
        return;
    }

    float texel_x = 1.0 / SourceSize.x; 

    // --- FETCH CENTER COLOR ---
    float raw_index = texture(tex, uv).b; // Using your working .b channel
    int index = int(clamp(raw_index * 255.0, 0.0, 15.0));
    vec3 col = texelFetch(paletteTex, ivec2(index, 0), 0).rgb;

    // --- FETCH LEFT COLOR ---
    float left_raw = texture(tex, uv - vec2(texel_x * BLUR_OFFSET, 0.0)).b;
    int left_index = int(clamp(left_raw * 255.0, 0.0, 15.0));
    vec3 left_col = texelFetch(paletteTex, ivec2(left_index, 0), 0).rgb;

    // --- FETCH RIGHT COLOR ---
    float right_raw = texture(tex, uv + vec2(texel_x * BLUR_OFFSET, 0.0)).b;
    int right_index = int(clamp(right_raw * 255.0, 0.0, 15.0));
    vec3 right_col = texelFetch(paletteTex, ivec2(right_index, 0), 0).rgb;

    // --- BLEND REAL RGB COLORS (Prevents index corruption & darkness) ---
    col = (col * 0.5) + (left_col * 0.25) + (right_col * 0.25);
    // 3. Linearize
    col = pow(col, vec3(INPUT_GAMMA));

    // 4. Smooth Scanlines
    float pos_y = uv.y * SourceSize.y;
    float delta_y = abs(fract(pos_y) - 0.5);
    float scanline = mix(1.0, SCANLINE_GAP_BRIGHTNESS, smoothstep(0.0, 0.5, delta_y * SCANLINE_WEIGHT));

    col *= scanline;
    col *= BLOOM_FACTOR;

    // 5. Gamma correction out
    f_color = vec4(pow(col, vec3(1.0 / OUTPUT_GAMMA)), 1.0);
}
"""


class CRTProcessor:
    def __init__(self, internal_res, output_res):
        self.ctx = moderngl.create_context()
        self.prog = self.ctx.program(
            vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER
        )

        # Assign Static Uniforms ONCE
        if "SourceSize" in self.prog:
            self.prog["SourceSize"].value = (
                internal_res[0],
                internal_res[1],
                1.0 / internal_res[0],
                1.0 / internal_res[1],
            )
        if "OutputSize" in self.prog:
            self.prog["OutputSize"].value = (
                output_res[0],
                output_res[1],
                1.0 / output_res[0],
                1.0 / output_res[1],
            )
        if "tex" in self.prog:
            self.prog["tex"].value = 0

        # Geometry Setup
        vertices = np.array(
            [
                -1.0,
                1.0,
                0.0,
                0.0,  # Maps Top-Left screen to Top-Left texture
                -1.0,
                -1.0,
                0.0,
                1.0,  # Maps Bottom-Left screen to Bottom-Left texture
                1.0,
                1.0,
                1.0,
                0.0,  # Maps Top-Right screen to Top-Right texture
                1.0,
                -1.0,
                1.0,
                1.0,  # Maps Bottom-Right screen to Bottom-Right texture
            ],
            dtype="f4",
        )

        self.vbo = self.ctx.buffer(vertices)
        self.vao = self.ctx.vertex_array(
            self.prog, [(self.vbo, "2f 2f", "in_vert", "in_uv")]
        )

        self.texture = self.ctx.texture(internal_res, 4)
        self.texture.filter = (moderngl.NEAREST, moderngl.NEAREST)

    def render(self, surface):
        # OPTIMIZATION: Use get_view to avoid string byte conversions/allocations
        self.texture.write(surface.get_view("2"))

        # Render pipeline execution
        self.texture.use(location=0)
        self.vao.render(moderngl.TRIANGLE_STRIP)
