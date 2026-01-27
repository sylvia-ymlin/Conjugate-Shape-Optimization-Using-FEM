from PIL import Image
import os

target_width = 400
images = [
    "AppliedFEM/ProblemB1_FinestMeshes.png",
    "AppliedFEM/ProblemB3_Solution_T_30.png",
    "AppliedFEM/Part3_Task2_Massloss.png",
    "simulation_result.png"
]

print(f"Forcing resize of images to width {target_width}px...")

for img_path in images:
    if os.path.exists(img_path):
        try:
            with Image.open(img_path) as img:
                current_width, current_height = img.size
                ratio = target_width / current_width
                new_height = int(current_height * ratio)
                
                # Always resize if current > target, or just do it to be safe if close
                if current_width > target_width:
                    print(f"Resizing {img_path}: {current_width}x{current_height} -> {target_width}x{new_height}")
                    img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)
                    img.save(img_path)
                else:
                    print(f"Skipping {img_path} (already small: {current_width}px)")
                    
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
    else:
        print(f"File not found: {img_path}")
