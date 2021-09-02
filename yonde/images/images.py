from PIL import Image, ImageFile
from pathlib import Path
from io import BytesIO
import natsort
import shutil
import glob
import os
ImageFile.LOAD_TRUNCATED_IMAGES = True


class Images(object):
    @staticmethod
    def manga_pdf_path(output_path, manga_name, pdf_name):
        return Path(Path.home(), manga_name, pdf_name) if not output_path else Path(output_path, manga_name, pdf_name)

    @staticmethod
    def create_path(path):
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    @staticmethod
    def remove_path(path):
        shutil.rmtree(path)

    @staticmethod
    def _make_pdf(files, save_path, pdf_name):
        images = [Image.open(f).convert('RGB') for f in files]
        images[0].save(Path(save_path, f'{pdf_name}.pdf'), save_all=True, subsampling=0, quality=80,
                       append_images=images[1:])

    @staticmethod
    def _remove_images(files):
        for i in files:
            os.remove(i)

    @staticmethod
    def _image_convert(content):
        png = Image.open(BytesIO(content)).convert('RGBA')
        background = Image.new('RGBA', png.size, (255, 255, 255))
        return Image.alpha_composite(background, png).convert("RGB")

    def image_save(self, path, nome, content, typo):
        if "pdf" in typo:
            converted = self._image_convert(content)
            converted.save(Path(path, f'{nome}.jpg'), 'JPEG', quality=100)
        else:
            with open(Path(path, f'{nome}.jpg'), 'wb') as f:
                f.write(content)

    def typo_checker(self, path_images, output_path, pdf_name, typo):
        filenames = natsort.natsorted([f for f in glob.iglob(str(Path(path_images, '*.jpg').resolve()))], reverse=False)
        if filenames:
            if typo == ["pdf", "imagens"] or typo == ["imagens", "pdf"]:  # Converter PDF e manter imagens.
                self._make_pdf(filenames, output_path, pdf_name)
            elif typo == ["pdf"]:  # Apenas converter PDF.
                self._make_pdf(filenames, output_path, pdf_name)
                self._remove_images(filenames)
            else:
                pass
