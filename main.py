import zipfile
import os
import shutil


class MTZManager:
    """
    کلاسی برای استخراج و بسته‌بندی فایل‌های تم شیائومی (.mtz)
    """
    def __init__(self, mtz_path):
        self.mtz_path = mtz_path

    def extract(self, output_dir=None):
        """
        استخراج محتویات فایل MTZ به یک پوشه
        """
        if not os.path.exists(self.mtz_path):
            print(f"❌ فایل یافت نشد: {self.mtz_path}")
            return False

        if output_dir is None:
            # ایجاد نام پوشه بر اساس نام فایل MTZ
            base_name = os.path.splitext(os.path.basename(self.mtz_path))[0]
            output_dir = f"{base_name}_extracted"

        if os.path.exists(output_dir):
            print(f"⚠️ پوشه از قبل وجود دارد: {output_dir}")
            response = input("آیا می‌خواهید آن را جایگزین کنید؟ (y/n): ")
            if response.lower() == 'y':
                shutil.rmtree(output_dir)
            else:
                print("عملیات لغو شد.")
                return False

        try:
            with zipfile.ZipFile(self.mtz_path, 'r') as zip_ref:
                zip_ref.extractall(output_dir)
            print(f"✅ استخراج با موفقیت انجام شد: {output_dir}")
            self._show_theme_info(output_dir)
            return True
        except zipfile.BadZipFile:
            print("❌ خطا: فایل مورد نظر یک آرشیو ZIP/MTZ معتبر نیست.")
            return False
        except Exception as e:
            print(f"❌ خطای غیرمنتظره در حین استخراج: {e}")
            return False

    def pack(self, source_dir, output_mtz=None):
        """
        بسته‌بندی یک پوشه به فایل MTZ
        """
        if not os.path.isdir(source_dir):
            print(f"❌ پوشه منبع یافت نشد: {source_dir}")
            return False

        if output_mtz is None:
            output_mtz = f"{os.path.basename(source_dir)}.mtz"

        # بررسی وجود فایل description.xml (الزامی برای تم)
        desc_path = os.path.join(source_dir, 'description.xml')
        if not os.path.isfile(desc_path):
            print("⚠️ هشدار: فایل description.xml در ریشه پوشه یافت نشد.")
            print("   این فایل برای شناسایی تم توسط گوشی الزامی است.")

        try:
            with zipfile.ZipFile(output_mtz, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # محاسبه مسیر نسبی برای حفظ ساختار پوشه در آرشیو
                        arcname = os.path.relpath(file_path, source_dir)
                        zipf.write(file_path, arcname)
            print(f"✅ بسته‌بندی با موفقیت انجام شد: {output_mtz}")
            return True
        except Exception as e:
            print(f"❌ خطا در حین بسته‌بندی: {e}")
            return False

    def _show_theme_info(self, extracted_dir):
        """
        تلاش برای خواندن و نمایش اطلاعات فایل description.xml
        """
        desc_path = os.path.join(extracted_dir, 'description.xml')
        if os.path.exists(desc_path):
            print("\n📄 اطلاعات تم (description.xml):")
            try:
                with open(desc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # نمایش خطوط کلیدی
                    for line in content.splitlines():
                        line = line.strip()
                        if any(tag in line for tag in ['<title>', '<designer>', '<version>', '<uiVersion>']):
                            print(f"   {line}")
            except Exception as e:
                print(f"   (خطا در خواندن فایل: {e})")
        else:
            print("\n⚠️ فایل description.xml یافت نشد.")


# ------------------- مثال استفاده -------------------
if __name__ == "__main__":
    # مسیر فایل MTZ خود را اینجا قرار دهید
    mtz_file = "path/to/your/theme.mtz"
    extract_folder = "my_theme_files"

    manager = MTZManager(mtz_file)

    # 1. استخراج فایل MTZ
    # manager.extract(extract_folder)

    # 2. بسته‌بندی مجدد پوشه به MTZ
    # manager.pack(extract_folder, "new_theme.mtz")
