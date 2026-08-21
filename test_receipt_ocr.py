import easyocr

image_path = r"C:\Users\konga\OneDrive\Desktop\RecipeChatbot\Ingredientimage.png"

reader = easyocr.Reader(['en'])

results = reader.readtext(image_path)

print("\nOCR Result:")
print("-" * 60)

if not results:
    print("No text detected.")
else:
    for bounding_box, text, confidence in results:
        print(f"{text} | confidence: {confidence:.2f}")