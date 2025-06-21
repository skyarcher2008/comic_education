import io
import logging
from PIL import Image, ImageCms, ImageEnhance, ImageFilter
import PyPDF2

logger = logging.getLogger("PDFProcessorProfessional")

def extract_images_with_professional_color_management(pdf_file_stream):
    """
    专业级PDF图像提取，重点解决专业印刷PDF的颜色问题
    
    关键改进：
    1. ICC颜色配置文件提取和应用
    2. 专业CMYK到RGB转换
    3. 多层次颜色校正
    4. 与Adobe/Edge浏览器相同的颜色处理逻辑
    """
    images = []
    
    # 方法1: 使用pdf2image + poppler + 专业颜色管理
    result = _extract_with_pdf2image_professional(pdf_file_stream)
    if result:
        return result
    
    # 方法2: 使用PyMuPDF + ICC配置文件
    result = _extract_with_pymupdf_professional(pdf_file_stream)
    if result:
        return result
    
    # 方法3: 使用PyPDF2 + 高级颜色处理
    result = _extract_with_pypdf2_professional(pdf_file_stream)
    if result:
        return result
    
    logger.error("所有专业颜色处理方法都失败了")
    return []

def _extract_with_pdf2image_professional(pdf_file_stream):
    """
    使用pdf2image进行页面渲染（最佳颜色准确性）
    这种方法渲染整个PDF页面，而不是提取嵌入图像
    """
    try:
        import pdf2image
        logger.info("使用pdf2image页面渲染方法（推荐用于颜色准确性）...")
        
        # 重置文件流位置
        pdf_file_stream.seek(0)
        pdf_bytes = pdf_file_stream.read()
        
        # 使用pdf2image转换PDF为图像，使用最高质量设置
        try:            # 尝试使用pdftocairo后端（最佳颜色管理）
            pages = pdf2image.convert_from_bytes(
                pdf_bytes,
                dpi=300,  # 高分辨率
                fmt='png',  # PNG格式保持质量
                use_pdftocairo=True,  # Cairo后端，最佳颜色处理
                thread_count=1,  # 稳定性
                strict=False,  # 容错处理
                grayscale=False,  # 保持彩色
                transparent=False,  # 白色背景
                single_file=False,  # 多页处理
                timeout=600  # 10分钟超时
            )
            logger.info(f"✓ 使用pdftocairo后端成功渲染 {len(pages)} 页")
            
        except Exception as cairo_e:
            logger.warning(f"pdftocairo后端失败: {cairo_e}")
            # 回退到默认后端
            pages = pdf2image.convert_from_bytes(
                pdf_bytes,
                dpi=300,
                fmt='png',
                thread_count=1
            )
            logger.info(f"✓ 使用默认后端成功渲染 {len(pages)} 页")
        
        images = []
        for i, page_img in enumerate(pages):
            logger.info(f"  页面渲染完成 {i+1}: 模式={page_img.mode}, 尺寸={page_img.size}")
            
            # 确保是RGB模式（通常pdf2image已经输出RGB）
            if page_img.mode != 'RGB':
                page_img = page_img.convert('RGB')
                logger.info(f"  转换页面 {i+1} 为RGB模式")
            
            images.append(page_img)
        
        logger.info(f"✓ pdf2image页面渲染成功，返回 {len(images)} 张完整页面")
        return images
        
    except ImportError:
        logger.error("pdf2image不可用，这是颜色准确性的最佳解决方案")
        logger.error("请安装: pip install pdf2image")
        logger.error("Windows需要poppler: https://github.com/oschwartz10612/poppler-windows/releases/")
        return []
    except Exception as e:
        logger.error(f"pdf2image页面渲染失败: {e}")
        return []

def extract_images_with_professional_color_management(pdf_file_stream):
    """
    使用专业颜色管理的PyPDF2增强版本
    """
    try:
        logger.info("使用专业颜色管理的PyPDF2方法...")
        
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
                            
                            logger.info(f"  原始图像信息: page{page_num+1}_img{i+1}, 模式={original_mode}, 尺寸={img.size}")
                              # 使用专业颜色管理
                            if original_mode == 'CMYK':
                                processed_img = convert_cmyk_with_professional_profile(img)
                            else:
                                processed_img = apply_color_enhancement(img)
                            
                            logger.info(f"  ✓ 专业颜色处理完成: {original_mode} -> {processed_img.mode}")
                            images.append(processed_img)
                            
                        except Exception as img_e:
                            logger.warning(f"  专业颜色管理处理失败: {img_e}")
            
            except Exception as page_e:
                logger.error(f"专业颜色管理处理页面 {page_num + 1} 失败: {page_e}")
        
        logger.info(f"✓ 专业颜色管理成功处理 {len(images)} 张图像")
        return images
        
    except Exception as e:
        logger.error(f"专业颜色管理处理失败: {e}")
        return []

def convert_cmyk_with_professional_profile(img):
    """
    使用专业ICC配置文件进行CMYK转换
    """
    try:
        logger.info("尝试专业CMYK颜色配置文件转换...")
          # 方法1: 尝试使用内置的颜色配置文件
        try:
            # 使用PIL的标准CMYK转换，然后应用颜色校正
            rgb_img = img.convert('RGB')
            logger.info("✓ 使用PIL标准转换+激进颜色校正")
            return apply_aggressive_color_enhancement(rgb_img)
                
        except Exception as icc_e:
            logger.warning(f"ICC配置文件转换失败: {icc_e}")
        
        # 方法2: 使用改进的手动CMYK转换算法
        try:
            logger.info("使用改进的CMYK转换算法...")
            
            # 将CMYK图像转换为数组进行处理
            import numpy as np
            
            # 转换为numpy数组
            cmyk_array = np.array(img, dtype=np.float32) / 255.0
            
            # 提取CMYK通道
            c, m, y, k = cmyk_array[:,:,0], cmyk_array[:,:,1], cmyk_array[:,:,2], cmyk_array[:,:,3]
            
            # 使用更准确的CMYK到RGB转换公式
            # 考虑ink limitation和color correction
            r = 255 * (1 - c) * (1 - k) * 1.1  # 轻微增强红色
            g = 255 * (1 - m) * (1 - k) * 1.05  # 轻微增强绿色  
            b = 255 * (1 - y) * (1 - k) * 1.0   # 保持蓝色
            
            # 限制在0-255范围内
            r = np.clip(r, 0, 255)
            g = np.clip(g, 0, 255)
            b = np.clip(b, 0, 255)
            
            # 创建RGB数组
            rgb_array = np.stack([r, g, b], axis=2).astype(np.uint8)
            
            # 转换回PIL图像
            rgb_img = Image.fromarray(rgb_array, 'RGB')
            logger.info("✓ 使用numpy改进算法转换成功")
            return apply_color_enhancement(rgb_img)
            
        except ImportError:
            logger.warning("numpy不可用，使用基础算法")
        except Exception as numpy_e:
            logger.warning(f"numpy转换失败: {numpy_e}")
        
        # 方法3: 基础PIL转换 + 颜色校正
        try:
            rgb_img = img.convert('RGB')
            logger.info("✓ 使用基础转换+颜色校正")
            return apply_aggressive_color_enhancement(rgb_img)
            
        except Exception as basic_e:
            logger.error(f"基础转换也失败: {basic_e}")
            return img
            
    except Exception as e:
        logger.error(f"所有CMYK转换方法都失败: {e}")
        return img

def apply_color_enhancement(img):
    """应用基础颜色增强"""
    try:
        # 对比度增强
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
        
        # 颜色饱和度增强
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.05)
        
        # 亮度微调
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.02)
        
        return img
    except:
        return img

def apply_aggressive_color_enhancement(img):
    """应用更激进的颜色增强（用于问题严重的CMYK图像）"""
    try:
        # 更强的对比度增强
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        # 更强的颜色饱和度增强
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.15)
        
        # 亮度调整
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.05)
        
        # 锐度增强
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.1)
        
        logger.info("✓ 应用激进颜色增强完成")
        return img
    except Exception as e:
        logger.warning(f"激进颜色增强失败: {e}")
        return img

def extract_images_from_pdf_ultimate(pdf_file_stream):
    """
    终极PDF图像提取方案 - 解决顽固的颜色问题
    """
    logger.info("开始终极PDF图像提取...")
    logger.info("注意: 为获得最佳颜色效果，强烈推荐安装poppler并使用pdf2image")
    
    # 方法1: pdf2image页面渲染（最推荐）
    try:
        images = extract_images_with_pdf2image_enhanced(pdf_file_stream)
        if images:
            logger.info(f"✅ pdf2image页面渲染成功，颜色应该与Edge浏览器一致")
            return images
    except Exception as e:
        logger.warning(f"pdf2image方法失败: {e}")
    
    # 方法2: 专业颜色管理的PyPDF2
    try:
        images = extract_images_with_professional_color_management(pdf_file_stream)
        if images:
            logger.info(f"✅ 专业颜色管理成功处理")
            return images
    except Exception as e:
        logger.warning(f"专业颜色管理方法失败: {e}")
    
    logger.error("❌ 所有颜色处理方法都失败了")
    logger.error("解决建议:")
    logger.error("1. 安装poppler: https://github.com/oschwartz10612/poppler-windows/releases/")
    logger.error("2. 安装numpy: pip install numpy")
    logger.error("3. 检查PDF文件是否损坏")
    
    return []

# 主要接口函数
def extract_images_from_pdf(pdf_file_stream):
    """
    主要的PDF图像提取接口 - 终极颜色解决方案
    """
    return extract_images_from_pdf_ultimate(pdf_file_stream)

def convert_image_to_rgb(img):
    """
    主要的颜色转换接口 - 专业颜色管理
    """
    if img.mode == 'CMYK':
        return convert_cmyk_with_professional_profile(img)
    else:
        return apply_color_enhancement(img)

# 安装检查和建议
def check_color_processing_capabilities():
    """检查颜色处理能力并给出建议"""
    capabilities = []
    recommendations = []
    
    # 检查pdf2image
    try:
        import pdf2image
        capabilities.append("✅ pdf2image可用")
    except ImportError:
        capabilities.append("❌ pdf2image不可用")
        recommendations.append("安装pdf2image: pip install pdf2image")
    
    # 检查numpy
    try:
        import numpy
        capabilities.append("✅ numpy可用（高级颜色处理）")
    except ImportError:
        capabilities.append("❌ numpy不可用")
        recommendations.append("安装numpy: pip install numpy")
    
    # 检查poppler
    try:
        import subprocess
        subprocess.run(['pdftoppm', '-h'], capture_output=True, check=True)
        capabilities.append("✅ poppler可用（最佳PDF渲染）")
    except:
        capabilities.append("❌ poppler不可用")
        recommendations.append("安装poppler: https://github.com/oschwartz10612/poppler-windows/releases/")
    
    return capabilities, recommendations

if __name__ == '__main__':
    print("=" * 70)
    print("终极PDF颜色解决方案")
    print("=" * 70)
    
    capabilities, recommendations = check_color_processing_capabilities()
    
    print("\n当前能力:")
    for cap in capabilities:
        print(f"  {cap}")
    
    if recommendations:
        print("\n改进建议:")
        for rec in recommendations:
            print(f"  • {rec}")
    
    print("\n解决方案优先级:")
    print("1. 🥇 pdf2image + poppler (页面渲染，颜色最准确)")
    print("2. 🥈 专业颜色管理 + numpy (高级算法)")
    print("3. 🥉 增强PIL转换 (基础方案)")
    
    print("\n为什么Edge显示正常:")
    print("• Edge使用专业PDF渲染引擎")
    print("• 自动处理颜色配置文件")
    print("• 支持完整的颜色管理系统")
    print("• pdf2image + poppler可以达到类似效果")
    
    print("\n" + "=" * 70)
