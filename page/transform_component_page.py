from poium import Element
from .transform_str_replace_page import TransformStrReplacePage


class TransformComponentPage(TransformStrReplacePage):
    merge_component = Element(xpath='//span[text()="合并"]', describe='合并组件')
    str_replace_component = Element(xpath='//span[text()="字符替换"]', describe='字符替换组件')
    null_replace_component = Element(xpath='//span[text()="空值转换"]', describe='空值转换组件')
