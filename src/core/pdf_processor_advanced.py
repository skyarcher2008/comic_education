import io
import logging
from PIL import Image, ImageCms
import PyPDF2
import pdf2image
import os
from pathlib import Path

# 可选导入PyMuPDF
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

logger = logging.getLogger("PDFProcessor")

class AdvancedPDFProcessor:
    """
    高级PDF处理器，专门处理出版物PDF的颜色问题
    支持多种PDF处理库和颜色管理方案
    """
    
    def __init__(self):
        self.available_methods = self._check_available_methods()
        logger.info(f"可用的PDF处理方法: {', '.join(self.available_methods)}")
      def _check_available_methods(self):
        """检查可用的PDF处理方法"""
        methods = []
        
        # 检查 pdf2image
        try:
            import pdf2image
            methods.append("pdf2image")
        except ImportError:
            pass
        
        # 检查 PyMuPDF
        if PYMUPDF_AVAILABLE:
            methods.append("pymupdf")
        
        # PyPDF2总是可用的（已在requirements.txt中）
        methods.append("pypdf2")
        
        return methods
    
    def convert_image_to_rgb_advanced(self, img, method="advanced"):
        """
        高级颜色转换，专门处理出版物CMYK颜色
        """
        try:
            original_mode = img.mode
            logger.debug(f"原始图像模式: {original_mode}, 尺寸: {img.size}")
            
            if img.mode == 'RGB':
                return img
            
            if img.mode == 'CMYK':
                logger.info(f"使用{method}方法转换CMYK图像...")
                
                if method == "advanced" and hasattr(ImageCms, 'createProfile'):
                    try:
                        # 方法1: 使用ICC配置文件进行精确转换
                        # 创建标准CMYK和sRGB配置文件
                        cmyk_profile = ImageCms.createProfile('CMYK')
                        rgb_profile = ImageCms.createProfile('sRGB')
                        
                        # 创建转换器
                        transform = ImageCms.buildTransformFromOpenProfiles(
                            cmyk_profile, rgb_profile, 'CMYK', 'RGB'
                        )
                        
                        # 执行转换
                        rgb_img = ImageCms.applyTransform(img, transform)
                        logger.info("✓ ICC配置文件转换成功")
                        return rgb_img
                        
                    except Exception as icc_e:
                        logger.warning(f"ICC转换失败: {icc_e}")
                
                # 方法2: 使用改进的CMYK转换算法
                try:
                    # 手动CMYK到RGB转换，考虑出版物特点
                    cmyk_pixels = img.load()
                    width, height = img.size
                    rgb_img = Image.new('RGB', (width, height))
                    rgb_pixels = rgb_img.load()
                    
                    for y in range(height):
                        for x in range(width):
                            c, m, y_val, k = cmyk_pixels[x, y]
                            
                            # 改进的CMYK到RGB转换公式
                            # 考虑出版物的特殊颜色特征
                            c = c / 255.0
                            m = m / 255.0  
                            y_val = y_val / 255.0
                            k = k / 255.0
                            
                            # 使用更准确的转换公式
                            r = 255 * (1 - c) * (1 - k)
                            g = 255 * (1 - m) * (1 - k)
                            b = 255 * (1 - y_val) * (1 - k)
                            
                            rgb_pixels[x, y] = (int(r), int(g), int(b))
                    
                    logger.info("✓ 手动CMYK转换成功")
                    return rgb_img
                    
                except Exception as manual_e:
                    logger.warning(f"手动转换失败: {manual_e}")
                
                # 方法3: PIL标准转换（最后的备选方案）
                try:
                    rgb_img = img.convert('RGB')
                    # 应用颜色校正
                    rgb_img = self._apply_color_correction(rgb_img)
                    logger.info("✓ 标准转换+颜色校正完成")
                    return rgb_img
                except Exception as std_e:
                    logger.warning(f"标准转换失败: {std_e}")
            
            # 处理其他颜色模式
            elif img.mode in ['L', 'LA', 'P', 'RGBA']:
                rgb_img = img.convert('RGB')
                return self._apply_color_correction(rgb_img)
            
            return img
            
        except Exception as e:
            logger.error(f"颜色转换失败: {e}")
            return img
    
    def _apply_color_correction(self, img):
        """应用颜色校正以改善出版物颜色"""
        try:
            from PIL import ImageEnhance
            
            # 轻微增强对比度和饱和度
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.1)
            
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.05)
            
            return img
        except:
            return img
    
    def extract_images_with_pdf2image(self, pdf_file_stream):
        """使用pdf2image提取图像（推荐用于出版物）"""
        try:
            logger.info("使用pdf2image方法提取PDF图像...")
            
            # 重置文件流位置
            pdf_file_stream.seek(0)
            pdf_bytes = pdf_file_stream.read()
            
            # 使用pdf2image转换PDF为图像，指定高分辨率
            pages = pdf2image.convert_from_bytes(
                pdf_bytes,
                dpi=300,  # 高分辨率，适合出版物
                fmt='png',  # PNG格式保持质量
                use_pdftocairo=True,  # 使用cairo后端获得更好的颜色
                thread_count=1  # 避免内存问题
            )
            
            images = []
            for i, page_img in enumerate(pages):
                logger.info(f"  pdf2image提取页面 {i+1}: 模式={page_img.mode}, 尺寸={page_img.size}")
                
                # 确保是RGB模式
                if page_img.mode != 'RGB':
                    page_img = page_img.convert('RGB')
                
                images.append(page_img)
            
            logger.info(f"pdf2image成功提取 {len(images)} 张图片")
            return images
            
        except Exception as e:
            logger.error(f"pdf2image提取失败: {e}")
            return []
    
    def extract_images_with_pymupdf(self, pdf_file_stream):
        """使用PyMuPDF提取图像"""
        try:
            logger.info("使用PyMuPDF方法提取PDF图像...")
            
            # 重置文件流位置
            pdf_file_stream.seek(0)
            pdf_bytes = pdf_file_stream.read()
            
            # 打开PDF
            pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            images = []
            
            for page_num in range(pdf_doc.page_count):
                page = pdf_doc[page_num]
                
                # 获取页面上的图像
                img_list = page.get_images()
                logger.debug(f"页面 {page_num + 1}: 发现 {len(img_list)} 个图像对象")
                
                for img_index, img in enumerate(img_list):
                    try:
                        # 提取图像数据
                        xref = img[0]
                        pix = fitz.Pixmap(pdf_doc, xref)
                        
                        # 处理不同的颜色空间
                        if pix.n - pix.alpha < 4:  # 不是CMYK
                            # 转换为RGB
                            if pix.colorspace and pix.colorspace.name != 'DeviceRGB':
                                pix = fitz.Pixmap(fitz.csRGB, pix)
                        else:  # CMYK图像
                            logger.info(f"  检测到CMYK图像，进行专门处理...")
                            pix = fitz.Pixmap(fitz.csRGB, pix)
                        
                        # 转换为PIL图像
                        img_data = pix.tobytes("png")
                        pil_img = Image.open(io.BytesIO(img_data))
                        
                        logger.info(f"  PyMuPDF提取图像: 页面{page_num+1}_图像{img_index+1} (模式: {pil_img.mode}, 尺寸: {pil_img.size})")
                        images.append(pil_img)
                        
                        pix = None  # 释放内存
                        
                    except Exception as img_e:
                        logger.warning(f"  PyMuPDF提取页面 {page_num + 1} 图像 {img_index + 1} 失败: {img_e}")
            
            pdf_doc.close()
            logger.info(f"PyMuPDF成功提取 {len(images)} 张图片")
            return images
            
        except Exception as e:
            logger.error(f"PyMuPDF提取失败: {e}")
            return []
    
    def extract_images_with_pypdf2_enhanced(self, pdf_file_stream):
        """使用增强的PyPDF2方法"""
        try:
            logger.info("使用增强PyPDF2方法提取PDF图像...")
            
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
                                
                                # 使用高级颜色转换
                                img = self.convert_image_to_rgb_advanced(img, method="advanced")
                                
                                logger.info(f"  增强PyPDF2提取图像: page{page_num+1}_img{i+1} (原始: {original_mode} -> {img.mode}, 尺寸: {img.size})")
                                images.append(img)
                                
                            except Exception as img_e:
                                logger.warning(f"  增强PyPDF2提取失败: {img_e}")
                
                except Exception as page_e:
                    logger.error(f"增强PyPDF2处理页面 {page_num + 1} 失败: {page_e}")
            
            logger.info(f"增强PyPDF2成功提取 {len(images)} 张图片")
            return images
            
        except Exception as e:
            logger.error(f"增强PyPDF2提取失败: {e}")
            return []
    
    def extract_images_from_pdf(self, pdf_file_stream):
        """
        智能PDF图像提取，自动选择最佳方法
        """
        logger.info("开始智能PDF图像提取...")
        
        # 按优先级尝试不同方法
        methods = [
            ("pdf2image", self.extract_images_with_pdf2image),
            ("pymupdf", self.extract_images_with_pymupdf), 
            ("pypdf2_enhanced", self.extract_images_with_pypdf2_enhanced)
        ]
        
        for method_name, method_func in methods:
            if method_name.replace("_enhanced", "").replace("_", "") in [m.replace("_", "") for m in self.available_methods]:
                try:
                    logger.info(f"尝试使用 {method_name} 方法...")
                    images = method_func(pdf_file_stream)
                    
                    if images:
                        logger.info(f"✓ {method_name} 成功提取 {len(images)} 张图片")
                        return images
                    else:
                        logger.warning(f"✗ {method_name} 未提取到图片")
                        
                except Exception as e:
                    logger.error(f"✗ {method_name} 方法失败: {e}")
                    continue
        
        logger.error("所有PDF处理方法都失败了")
        return []


# 保持向后兼容的函数
def extract_images_from_pdf(pdf_file_stream):
    """向后兼容的函数接口"""
    processor = AdvancedPDFProcessor()
    return processor.extract_images_from_pdf(pdf_file_stream)


def convert_image_to_rgb(img):
    """向后兼容的颜色转换函数"""
    processor = AdvancedPDFProcessor()
    return processor.convert_image_to_rgb_advanced(img)
