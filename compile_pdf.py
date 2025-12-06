#!/usr/bin/env python3
"""
Compile all page overlays into the final GPT Wrapped PDF.
"""
from pypdf import PdfReader, PdfWriter
import importlib.util
import sys

# PDF settings
INPUT_PDF = "Green and Orange Dynamic 2025 Company Wrapped Annual report Presentation-2.pdf"
OUTPUT_PDF = "gpt_wrapped_2025_final.pdf"

# Page modules to load (page number -> module name)
PAGE_MODULES = {
    3: "page3_words",
    4: "page4_streak",
    5: "page5_top_words",
    6: "page6_pie_chart",
    7: "page7_longest_chat",
    8: "page8_monthly_chart",
    9: "page9_heatmap",
    10: "page10_prompts",
    11: "page11_persona",
    12: "page12_summary",
}

def load_module(module_name):
    """Dynamically load a module."""
    spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def main():
    print("=" * 60)
    print("GPT WRAPPED 2025 - PDF COMPILER")
    print("=" * 60)
    
    # First run data extractor
    print("\n📊 Step 1: Extracting data from conversations...")
    extractor = load_module("data_extractor")
    extractor.main()
    
    # Open the template PDF
    print(f"\n📄 Step 2: Opening template PDF...")
    reader = PdfReader(INPUT_PDF)
    writer = PdfWriter()
    
    print(f"   Template has {len(reader.pages)} pages")
    
    # Process each page
    print(f"\n🎨 Step 3: Creating and applying overlays...")
    
    for i, page in enumerate(reader.pages):
        page_num = i + 1
        
        if page_num in PAGE_MODULES:
            module_name = PAGE_MODULES[page_num]
            print(f"   Page {page_num}: Loading {module_name}...")
            
            try:
                module = load_module(module_name)
                overlay_bytes = module.create_overlay()
                overlay_reader = PdfReader(overlay_bytes)
                
                if len(overlay_reader.pages) > 0:
                    page.merge_page(overlay_reader.pages[0])
                    print(f"   Page {page_num}: ✅ Overlay applied")
                else:
                    print(f"   Page {page_num}: ⚠️ Empty overlay")
            except Exception as e:
                print(f"   Page {page_num}: ❌ Error - {e}")
        else:
            print(f"   Page {page_num}: ⏭️ No overlay needed")
        
        writer.add_page(page)
    
    # Save the final PDF
    print(f"\n💾 Step 4: Saving to {OUTPUT_PDF}...")
    with open(OUTPUT_PDF, "wb") as f:
        writer.write(f)
    
    print("\n" + "=" * 60)
    print("✅ GPT WRAPPED 2025 PDF COMPLETE!")
    print(f"   Output: {OUTPUT_PDF}")
    print("=" * 60)

if __name__ == "__main__":
    main()

