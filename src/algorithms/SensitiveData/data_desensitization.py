import re
import os
import logging
import json
import pandas as pd
from typing import Dict, Optional

class SensitiveDataAnonymizer:
    """敏感数据脱敏工具"""

    def __init__(self):
        self.logger = self._setup_logger()
        self.patterns = self._load_patterns()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger('SensitiveDataAnonymizer')
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _load_patterns(self) -> Dict[str, Dict]:
        return {
            "id_card": {
                "pattern": r"[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[0-9Xx]",
                "anonymize": self._anonymize_id_card
            },
            "phone": {
                "pattern": r"1[3-9]\d{9}",
                "anonymize": self._anonymize_phone
            },
            "email": {
                "pattern": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}",
                "anonymize": self._anonymize_email
            },
            "credit_card": {
                "pattern": r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3[0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b",
                "anonymize": self._anonymize_credit_card
            },
            "bank_card": {
                "pattern": r"[1-9]\d{15,18}",
                "anonymize": self._anonymize_bank_card
            },
            "ip_address": {
                "pattern": r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",
                "anonymize": self._anonymize_ip
            }
        }

    def _anonymize_id_card(self, value: str) -> str:
        return value[:6] + '*' * (len(value) - 10) + value[-4:]

    def _anonymize_phone(self, value: str) -> str:
        return value[:3] + '****' + value[7:]

    def _anonymize_email(self, value: str) -> str:
        parts = value.split('@')
        username = parts[0]
        domain = parts[1]
        if len(username) > 3:
            return username[0] + '*' * (len(username) - 2) + username[-1] + '@' + domain
        return username[0] + '*' * (len(username) - 1) + '@' + domain

    def anonymize_name(self, value: str) -> str:
        if len(value) > 1:
            return value[0] + '*' * (len(value) - 1)
        return value

    def _anonymize_credit_card(self, value: str) -> str:
        return value[:6] + '*' * (len(value) - 10) + value[-4:]

    def _anonymize_bank_card(self, value: str) -> str:
        return value[:6] + '*' * (len(value) - 10) + value[-4:]

    def _anonymize_ip(self, value: str) -> str:
        parts = value.split('.')
        return f"{parts[0]}.{parts[1]}.**.**"

    def anonymize_text(self, text: str) -> str:
        name_pattern = re.compile(r"(?<!\S)([A-Z][a-z]+ [A-Z][a-z]+)|([一-龥]{2,})(?!\S)")
        text = name_pattern.sub(lambda match: self.anonymize_name(match.group()), text)

        for key, conf in self.patterns.items():
            regex = re.compile(conf["pattern"])
            text = regex.sub(lambda m: conf["anonymize"](m.group()), text)
        return text

    def anonymize_file(self, input_path: str, output_path: Optional[str] = None) -> Optional[str]:
        if not os.path.exists(input_path):
            self.logger.error(f"文件不存在: {input_path}")
            return None

        if not output_path:
            file_dir, file_name = os.path.split(input_path)
            file_base, file_ext = os.path.splitext(file_name)
            output_path = os.path.join(file_dir, f"{file_base}_anonymized{file_ext}")

        try:
            if input_path.endswith('.txt'):
                self._anonymize_txt_file(input_path, output_path)
            elif input_path.endswith('.csv'):
                self._anonymize_csv_file(input_path, output_path)
            elif input_path.endswith(('.xlsx', '.xls')):
                self._anonymize_excel_file(input_path, output_path)
            elif input_path.endswith('.json'):
                self._anonymize_json_file(input_path, output_path)
            else:
                self.logger.warning(f"不支持的文件类型: {input_path}")
                return None

            self.logger.info(f"文件脱敏完成: {output_path}")
            return output_path

        except Exception as e:
            self.logger.error(f"文件脱敏失败: {e}")
            return None

    def _anonymize_txt_file(self, input_path: str, output_path: str):
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        anonymized = self.anonymize_text(content)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(anonymized)

    def _anonymize_csv_file(self, input_path: str, output_path: str):
        df = pd.read_csv(input_path, encoding='utf-8', low_memory=False)
        for col in df.columns:
            df[col] = df[col].apply(lambda x: self.anonymize_text(str(x)) if pd.notna(x) else x)
        df.to_csv(output_path, index=False, encoding='utf-8')

    def _anonymize_excel_file(self, input_path: str, output_path: str):
        ext = os.path.splitext(input_path)[1].lower()
        engine = 'xlrd' if ext == '.xls' else 'openpyxl'
        with pd.ExcelFile(input_path, engine=engine) as xls:
            sheets = {name: pd.read_excel(xls, sheet_name=name, engine=engine) for name in xls.sheet_names}
        for df in sheets.values():
            for col in df.columns:
                df[col] = df[col].apply(lambda x: self.anonymize_text(str(x)) if pd.notna(x) else x)
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for name, df in sheets.items():
                df.to_excel(writer, sheet_name=name, index=False)

    def _anonymize_json_file(self, input_path: str, output_path: str):
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        def traverse(obj):
            if isinstance(obj, dict):
                return {k: traverse(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [traverse(item) for item in obj]
            elif isinstance(obj, str):
                return self.anonymize_text(obj)
            return obj

        anonymized_data = traverse(data)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(anonymized_data, f, ensure_ascii=False, indent=2)

# 提供前端调用的函数
def run_from_path(input_path: str) -> str:
    anonymizer = SensitiveDataAnonymizer()
    if not os.path.exists(input_path):
        return f"文件不存在：{input_path}"

    result = anonymizer.anonymize_file(input_path)
    if result:
        return f"脱敏完成！结果保存至：{result}"
    return "脱敏失败，请检查文件格式或内容。"
