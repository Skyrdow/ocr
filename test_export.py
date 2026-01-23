import os
import sys
from processor import save_to_file

def test_exports():
    print("Testing exports...")
    
    sample_text = "Esta es una prueba de exportación.\nLínea 2 de prueba."
    output_dir = "test_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    formats = ["docx", "pdf"]
    
    for fmt in formats:
        output_path = os.path.join(output_dir, f"test_output_v2.{fmt}")
        try:
            print(f"Testing {fmt} export to {output_path}...")
            save_to_file(sample_text, output_path, fmt)
            
            if os.path.exists(output_path):
                size = os.path.getsize(output_path)
                print(f"✅ SUCCESS: {fmt} file created (Size: {size} bytes)")
            else:
                print(f"❌ FAILURE: {fmt} file not found after save.")
                
        except Exception as e:
            print(f"❌ ERROR testing {fmt}: {e}")
            import traceback
            traceback.print_exc()

    # Verify TXT raises error
    try:
        print("Testing TXT export (should fail)...")
        save_to_file(sample_text, "fail.txt", "txt")
        print("❌ FAILURE: TXT export should have raised ValueError")
    except ValueError:
        print("✅ SUCCESS: TXT export raised ValueError as expected")

if __name__ == "__main__":
    test_exports()
