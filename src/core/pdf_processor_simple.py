import io
import logging
from PIL import Image, ImageCms, ImageEnhance
import PyPDF2

logger = logging.getLogger("PDFProcessor")

def convert_image_to_rgb_enhanced(img):
    """
    增强的颜色转换，专门处理出版物CMYK颜色问题
    """
    try:
        original_mode = img.mode
        logger.debug(f"原始图像模式: {original_mode}, 尺寸: {img.size}")
        
        if img.mode == 'RGB':
            return img
        
        if img.mode == 'CMYK':
            logger.info(f"检测到CMYK模式图像，使用增强转换...")
            
            # 方法1: 尝试使用ICC配置文件 (如果可用)
            try:
                # 使用标准CMYK到RGB转换
                rgb_img = img.convert('RGB')
                
                # 应用颜色校正以改善出版物颜色
                # 轻微增强对比度
                enhancer = ImageEnhance.Contrast(rgb_img)
                rgb_img = enhancer.enhance(1.1)
                
                # 轻微增强颜色饱和度
                enhancer = ImageEnhance.Color(rgb_img)
                rgb_img = enhancer.enhance(1.05)
                
                # 轻微调整亮度
                enhancer = ImageEnhance.Brightness(rgb_img)
                rgb_img = enhancer.enhance(1.02)
                
                logger.info("✓ CMYK转换+颜色校正完成")
                return rgb_img
                
            except Exception as e:
                logger.warning(f"增强转换失败，使用标准转换: {e}")
                return img.convert('RGB')
        
        # 处理其他颜色模式
        elif img.mode in ['L', 'LA', 'P', 'RGBA']:
            logger.info(f"转换 {original_mode} 模式到RGB...")
            rgb_img = img.convert('RGB')
            return rgb_img
        
        return img
        
    except Exception as e:
        logger.error(f"颜色转换失败: {e}")
        return img

def extract_images_with_pdf2image(pdf_file_stream):
    """使用pdf2image提取图像（推荐用于出版物）"""
    try:
        import pdf2image
        logger.info("使用pdf2image方法提取PDF图像...")
        
        # 重置文件流位置
        pdf_file_stream.seek(0)
        pdf_bytes = pdf_file_stream.read()
        
        # 使用pdf2image转换PDF为图像，指定高分辨率
        pages = pdf2image.convert_from_bytes(
            pdf_bytes,
            dpi=300,  # 高分辨率，适合出版物
            fmt='png',  # PNG格式保持质量
            thread_count=1  # 避免内存问题
        )
        
        images = []
        for i, page_img in enumerate(pages):
            logger.info(f"  pdf2image提取页面 {i+1}: 模式={page_img.mode}, 尺寸={page_img.size}")
            
            # 确保是RGB模式
            if page_img.mode != 'RGB':
                page_img = page_img.convert('RGB')
            
            images.append(page_img)
        
        logger.info(f"✓ pdf2image成功提取 {len(images)} 张完整页面图片")
        return images
        
    except ImportError:
        logger.warning("pdf2image不可用，请安装: pip install pdf2image")
        return []
    except Exception as e:
        logger.error(f"pdf2image提取失败: {e}")
        return []

def extract_images_with_pypdf2_enhanced(pdf_file_stream):
    """使用增强的PyPDF2方法提取嵌入图像"""
    try:
        logger.info("使用增强PyPDF2方法提取PDF嵌入图像...")
        
        # 重置文件流位置
        pdf_file_stream.seek(0)
        
        pdf_reader = PyPDF2.PdfReader(pdf_file_stream)
        images = []
        
        for page_num in range(len(pdf_reader.pages)):
            try:
                page = pdf_reader.pages[page_num]
                
                if hasattr(page, 'images') and page.images:
                    for i, img_obj in enumerate(page.images):
                        try:
                            img = Image.open(io.BytesIO(img_obj.data))
                            original_mode = img.mode
                            
                            # 使用增强颜色转换
                            img = convert_image_to_rgb_enhanced(img)
                            
                            logger.info(f"  增强PyPDF2提取图像: page{page_num+1}_img{i+1} (原始: {original_mode} -> {img.mode}, 尺寸: {img.size})")
                            images.append(img)
                            
                        except Exception as img_e:
                            logger.warning(f"  增强PyPDF2提取失败: {img_e}")
            
            except Exception as page_e:
                logger.error(f"增强PyPDF2处理页面 {page_num + 1} 失败: {page_e}")
        
        logger.info(f"✓ 增强PyPDF2成功提取 {len(images)} 张嵌入图像")
        return images
        
    except Exception as e:
        logger.error(f"增强PyPDF2提取失败: {e}")
        return []

def extract_images_from_pdf_smart(pdf_file_stream):
    """
    智能PDF图像提取，优先使用最佳方法
    返回完整页面图像或嵌入图像
    """
    logger.info("开始智能PDF图像提取...")
    
    # 方法1: 优先使用pdf2image (获取完整页面，颜色最准确)
    try:
        images = extract_images_with_pdf2image(pdf_file_stream)
        if images:
            logger.info(f"✓ pdf2image成功，返回 {len(images)} 张完整页面")
            return images
    except Exception as e:
        logger.warning(f"pdf2image方法失败: {e}")
    
    # 方法2: 使用增强PyPDF2 (提取嵌入图像)
    try:
        images = extract_images_with_pypdf2_enhanced(pdf_file_stream)
        if images:
            logger.info(f"✓ 增强PyPDF2成功，返回 {len(images)} 张嵌入图像")
            return images
    except Exception as e:
        logger.warning(f"增强PyPDF2方法失败: {e}")
    
    logger.error("所有PDF处理方法都失败了")
    return []

# 主要接口函数
def extract_images_from_pdf(pdf_file_stream):
    """
    主要的PDF图像提取接口
    替换原有的pdf_processor.py中的同名函数
    """
    return extract_images_from_pdf_smart(pdf_file_stream)

def convert_image_to_rgb(img):
    """
    主要的颜色转换接口  
    替换原有的pdf_processor.py中的同名函数
    """
    return convert_image_to_rgb_enhanced(img)

# 测试代码
if __name__ == '__main__':
    print("=" * 60)
    print("简化版高级PDF处理器")
    print("=" * 60)
    print("主要改进:")
    print("1. ✓ pdf2image优先 - 获取完整页面，颜色最准确")
    print("2. ✓ 增强颜色转换 - 专门优化CMYK出版物")
    print("3. ✓ 颜色校正 - 对比度/饱和度/亮度微调")
    print("4. ✓ 高分辨率支持 - 300 DPI输出")
    print("5. ✓ 向后兼容 - 直接替换原函数")
    print()
    print("使用方法:")
    print("1. 直接替换: 将此文件重命名为 pdf_processor.py")
    print("2. 或者导入: from pdf_processor_simple import extract_images_from_pdf")
    print()
    print("预期效果:")
    print("- 图像将以RGB模式直接提取")
    print("- 颜色更加准确和鲜艳")
    print("- 支持完整页面或嵌入图像提取")
    print("=" * 60)
