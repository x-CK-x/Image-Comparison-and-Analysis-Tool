import gradio as gr
from PIL import Image, ImageChops, ImageFilter, ImageOps
import numpy as np
import os

def resize_to_match(img, target_size):
    """Resize image to match the target size."""
    return img.resize(target_size, Image.LANCZOS)

def get_alpha_layer(img):
    """Extract the alpha layer of an image."""
    return img.getchannel('A') if img.mode == 'RGBA' else Image.new('L', img.size, 255)

def create_blank_image(size):
    """Create a blank (white) image with the given size."""
    return Image.new('RGB', size, color='white')

def process_images(ref_image_path, tgt_image_path, operation, alpha_value, output_dir,
                   flip_order, view_alpha, use_alpha_only,
                   invert_ref, invert_tgt, save_inverted,
                   create_blank_ref, create_blank_tgt):
    """Process images based on the selected operation and save the result."""
    # Load images
    if ref_image_path is not None and not create_blank_ref:
        ref_image = Image.open(ref_image_path)
    elif create_blank_ref and tgt_image_path is not None:
        tgt_image_temp = Image.open(tgt_image_path)
        ref_image = create_blank_image(tgt_image_temp.size)
    else:
        ref_image = None

    if tgt_image_path is not None and not create_blank_tgt:
        tgt_image = Image.open(tgt_image_path)
    elif create_blank_tgt and ref_image_path is not None:
        ref_image_temp = Image.open(ref_image_path)
        tgt_image = create_blank_image(ref_image_temp.size)
    else:
        tgt_image = None

    if ref_image is None:
        return None, "Please provide a reference image or create a blank one."
    if tgt_image is None and operation in ["Resize Target to Match Reference", "Add Images", "Subtract Images", 
                                           "Blend Images", "Histogram Comparison"]:
        return None, "Please provide a target image or create a blank one."

    # Resize target image to match reference image dimensions
    if tgt_image and tgt_image.size != ref_image.size:
        tgt_image = resize_to_match(tgt_image, ref_image.size)

    # Invert images if selected
    if invert_ref:
        ref_image = ImageOps.invert(ref_image.convert('RGB'))
        if save_inverted and output_dir:
            save_image(ref_image, ref_image_path, output_dir, suffix='-inverted')

    if invert_tgt and tgt_image:
        tgt_image = ImageOps.invert(tgt_image.convert('RGB'))
        if save_inverted and output_dir:
            save_image(tgt_image, tgt_image_path, output_dir, suffix='-inverted')

    # Handle alpha layer viewing
    if view_alpha:
        ref_image = get_alpha_layer(ref_image)
        if tgt_image:
            tgt_image = get_alpha_layer(tgt_image)
    else:
        # Ensure images are in 'RGB' mode
        ref_image = ref_image.convert('RGB')
        if tgt_image:
            tgt_image = tgt_image.convert('RGB')

    # Use only alpha layers for operations
    if use_alpha_only:
        ref_image = get_alpha_layer(ref_image)
        if tgt_image:
            tgt_image = get_alpha_layer(tgt_image)

    # Flip operation order if checkbox is checked
    if flip_order and tgt_image:
        ref_image, tgt_image = tgt_image, ref_image

    # Perform the selected operation
    if operation == "Resize Target to Match Reference":
        result_image = tgt_image
    elif operation == "Add Images":
        result_image = ImageChops.add(ref_image, tgt_image)
    elif operation == "Subtract Images":
        result_image = ImageChops.subtract(ref_image, tgt_image)
    elif operation == "Blend Images":
        result_image = Image.blend(ref_image, tgt_image, alpha_value)
    elif operation == "Edge Detection on Reference":
        result_image = edge_detection(ref_image)
    elif operation == "Histogram Comparison":
        result = histogram_compare(ref_image, tgt_image)
        return None, result
    else:
        result_image = ref_image

    # Save the result image
    message = save_image(result_image, ref_image_path, output_dir)
    return result_image, message

def save_image(image, original_path, output_dir, suffix='-test'):
    """Save the image to the output directory with modified name."""
    if output_dir:
        output_dir = output_dir.strip()
        if not output_dir:
            return "Output directory is empty. Please provide a valid path."
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Check if the directory is writable
            if not os.access(output_dir, os.W_OK):
                return f"Output directory '{output_dir}' is not writable."

            # Get the original image filename
            original_name = os.path.basename(original_path)
            name, ext = os.path.splitext(original_name)
            output_filename = f"{name}{suffix}.png"
            output_path = os.path.join(output_dir, output_filename)

            # Save image
            image.save(output_path, format='PNG')
            return f"Image saved to {output_path}"
        except Exception as e:
            return f"Error saving image: {e}"
    else:
        return "Operation completed successfully."

def edge_detection(image):
    """Apply edge detection filter to the image."""
    return image.convert("L").filter(ImageFilter.FIND_EDGES)

def histogram_compare(ref_img, tgt_img):
    """Compare histograms of two images."""
    hist1 = ref_img.histogram()
    hist2 = tgt_img.histogram()
    diff = sum(abs(h1 - h2) for h1, h2 in zip(hist1, hist2))
    return f"Histogram difference: {diff}"

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Image Comparison and Analysis Tool")

    with gr.Row():
        ref_image = gr.Image(type="filepath", label="Reference Image")
        tgt_image = gr.Image(type="filepath", label="Target Image")

    operation = gr.Radio(
        ["Resize Target to Match Reference", "Add Images", "Subtract Images", 
         "Blend Images", "Edge Detection on Reference", "Histogram Comparison"],
        label="Select Operation"
    )

    alpha_value = gr.Slider(0.0, 1.0, value=0.5, step=0.01, label="Blend Alpha", visible=False)

    with gr.Row():
        flip_order = gr.Checkbox(label="Flip Operation Order (Target Operation Reference)", value=False)
        view_alpha = gr.Checkbox(label="View Alpha Layers", value=False)
        use_alpha_only = gr.Checkbox(label="Use Alpha Layer Only for Operations", value=False)

    with gr.Row():
        invert_ref = gr.Checkbox(label="Invert Reference Image", value=False)
        invert_tgt = gr.Checkbox(label="Invert Target Image", value=False)
        save_inverted = gr.Checkbox(label="Save Inverted Images", value=False)

    with gr.Row():
        create_blank_ref = gr.Checkbox(label="Create Blank Reference Image", value=False)
        create_blank_tgt = gr.Checkbox(label="Create Blank Target Image", value=False)

    output_dir = gr.Textbox(label="Output Directory", placeholder="Enter the path to save the output image")

    run_button = gr.Button("Run Operation")

    with gr.Row():
        output_image = gr.Image(label="Output Image")
        output_text = gr.Textbox(label="Output Message")

    def update_ui(operation):
        if operation == "Blend Images":
            return gr.update(visible=True)
        else:
            return gr.update(visible=False)

    operation.change(update_ui, inputs=operation, outputs=[alpha_value])

    run_button.click(
        process_images,
        inputs=[ref_image, tgt_image, operation, alpha_value, output_dir,
                flip_order, view_alpha, use_alpha_only,
                invert_ref, invert_tgt, save_inverted,
                create_blank_ref, create_blank_tgt],
        outputs=[output_image, output_text]
    )

demo.launch()
