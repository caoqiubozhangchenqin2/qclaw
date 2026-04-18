import sys
try:
    from PIL import ImageGrab
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "pillow", "-q"])
    from PIL import ImageGrab

img = ImageGrab.grab()
img.save("C:/Users/Administrator/.qclaw/workspace-agent-71ec60f0/screen_pil.png")
print("Screenshot saved:", img.size)
