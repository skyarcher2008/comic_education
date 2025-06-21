import io
import logging
from PIL import Image, ImageCms
import PyPDF2 

logger = logging.getLogger("PDFProcessor")

def convert_image_to_rgb(img):
    """
    将图像转换为RGB模式，处理各种颜色空间问题。
    
    Args:
        img: PIL Image对象
        
    Returns:
        PIL Image对象，RGB模式
    """
    try:
        original_mode = img.mode
        logger.debug(f"原始图像模式: {original_mode}, 尺寸: {img.size}")
        
        # 如果已经是RGB模式，直接返回
        if img.mode == 'RGB':
            logger.debug("图像已是RGB模式，无需转换")
            return img
        
        # 处理CMYK模式
        if img.mode == 'CMYK':
            logger.info(f"检测到CMYK模式图像，转换为RGB...")
            
            # 尝试使用更精确的颜色转换
            try:
                # 使用PIL的标准CMYK到RGB转换
                rgb_img = img.convert('RGB')
                logger.info("成功转换CMYK到RGB")
                return rgb_img
            except Exception as convert_e:
                logger.warning(f"CMYK转换失败: {convert_e}")
                # 如果转换失败，创建一个新的RGB图像
                rgb_img = Image.new('RGB', img.size, color='white')
                logger.warning("使用白色背景作为fallback")
                return rgb_img
        
        # 处理其他颜色模式
        elif img.mode in ['L', 'LA', 'P', 'RGBA']:
            logger.info(f"转换 {original_mode} 模式到RGB...")
            rgb_img = img.convert('RGB')
            logger.info(f"颜色模式转换完成: {original_mode} -> {rgb_img.mode}")
            return rgb_img
        
        # 处理LAB等其他颜色空间
        elif img.mode == 'LAB':
            logger.info("检测到LAB颜色空间，转换为RGB...")
            try:
                rgb_img = img.convert('RGB')
                logger.info("LAB到RGB转换成功")
                return rgb_img
            except Exception as lab_e:
                logger.warning(f"LAB转换失败: {lab_e}")
                return img
        
        # 对于其他未知模式，尝试直接转换
        else:
            logger.warning(f"未知颜色模式 {original_mode}，尝试直接转换为RGB")
            rgb_img = img.convert('RGB')
            logger.info(f"转换完成: {original_mode} -> {rgb_img.mode}")
            return rgb_img
            
    except Exception as e:
        logger.error(f"颜色转换过程中发生错误: {e}")
        # 如果转换失败，尝试最基本的转换
        try:
            return img.convert('RGB')
        except:
            logger.error("所有颜色转换方法都失败，返回原始图像")
            return img

def extract_images_from_pdf(pdf_file_stream):
    """
    从 PDF 文件流中提取图像。

    Args:
        pdf_file_stream: PDF 文件的文件流对象 (例如通过 request.files 获取)。

    Returns:
        list: 包含提取出的 PIL Image 对象的列表。
    """
    images = []
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file_stream)
        num_pages = len(pdf_reader.pages)
        logger.info(f"开始处理 PDF 文件，共 {num_pages} 页。")

        for page_num in range(num_pages):
            try:
                page = pdf_reader.pages[page_num]
                # PyPDF2 >= 3.0.0 使用 page.images
                if hasattr(page, 'images') and page.images:
                    logger.debug(f"页面 {page_num + 1}: 发现 {len(page.images)} 个图像对象 (新方法)。")
                    for i, img_obj in enumerate(page.images):
                        try:
                            # img_obj.data 是图像的字节数据
                            img = Image.open(io.BytesIO(img_obj.data))
                            original_mode = img.mode
                            
                            # 转换为RGB模式以确保颜色正确
                            img = convert_image_to_rgb(img)
                            
                            # 尝试获取原始文件名（可能没有）
                            img_name = img_obj.name if hasattr(img_obj, 'name') else f"page{page_num+1}_img{i+1}"
                            logger.info(f"  成功提取图像: {img_name} (原始模式: {original_mode} -> {img.mode}, 尺寸: {img.size})")
                            images.append(img)
                        except Exception as img_e:
                            logger.warning(f"  提取页面 {page_num + 1} 的图像 {i+1} 失败: {img_e}")
                
                # 兼容旧版 PyPDF2 或不同结构的 PDF - 简化处理
                else:
                    try:
                        # 尝试从页面资源中提取图像
                        if hasattr(page, 'get') and '/Resources' in str(page):
                            logger.debug(f"页面 {page_num + 1}: 尝试使用旧方法提取图像...")
                            # 这里我们简化处理，避免复杂的PyPDF2对象访问
                    except Exception as resources_e:
                        logger.debug(f"页面 {page_num + 1} 旧方法提取失败: {resources_e}")

            except Exception as page_e:
                logger.error(f"处理 PDF 页面 {page_num + 1} 时出错: {page_e}", exc_info=True)

        logger.info(f"PDF 处理完成，共提取 {len(images)} 张图片。")
        return images

    except Exception as pdf_err:
        logger.error(f"无法读取 PDF 文件: {pdf_err}")
        return []

# --- 测试代码 ---
if __name__ == '__main__':
    try:
        from src.shared.path_helpers import resource_path, get_debug_dir
    except ImportError:
        # 如果导入失败，定义简单的替代函数
        def resource_path(path):
            return path
        def get_debug_dir(name):
            return f"debug_{name}"
    
    import os

    print("--- 测试 PDF 处理器 ---")
    # 需要一个测试 PDF 文件路径
    test_pdf_path = resource_path('docs/example.pdf') # 替换为你的测试 PDF 文件路径

    if os.path.exists(test_pdf_path):
        print(f"加载测试 PDF: {test_pdf_path}")
        try:
            with open(test_pdf_path, 'rb') as f:
                extracted_images = extract_images_from_pdf(f)
            print(f"提取完成，共找到 {len(extracted_images)} 张图片。")

            # 保存提取的图片用于检查 (可选)
            if extracted_images:
                save_dir = get_debug_dir("pdf_extracted_images")
                print(f"将提取的图片保存到: {save_dir}")
                os.makedirs(save_dir, exist_ok=True)
                for i, img in enumerate(extracted_images):
                    try:
                        img.save(os.path.join(save_dir, f"extracted_image_{i+1}.png"))
                    except Exception as save_e:
                        print(f"  保存图片 {i+1} 失败: {save_e}")
        except Exception as e:
            print(f"测试过程中发生错误: {e}")
    else:
        print(f"错误：测试 PDF 文件未找到 {test_pdf_path}")