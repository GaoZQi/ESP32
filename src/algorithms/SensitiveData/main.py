#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
敏感数据识别系统
支持多种敏感数据类型的检测和识别
"""

import re
import json
import hashlib
import logging
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum
import pandas as pd
import os
from datetime import datetime


class SensitiveDataType(Enum):
    """敏感数据类型枚举"""

    ID_CARD = "身份证号"
    PHONE = "手机号码"
    EMAIL = "邮箱地址"
    CREDIT_CARD = "信用卡号"
    BANK_CARD = "银行卡号"
    IP_ADDRESS = "IP地址"
    MAC_ADDRESS = "MAC地址"
    PASSPORT = "护照号码"
    SOCIAL_SECURITY = "社会保障号"
    LICENSE_PLATE = "车牌号"
    ORGANIZATION_CODE = "组织机构代码"
    TAX_NUMBER = "税务登记号"
    CUSTOM = "自定义规则"


@dataclass
class DetectionResult:
    """检测结果数据类"""

    data_type: SensitiveDataType
    value: str
    position: Tuple[int, int]  # (开始位置, 结束位置)
    confidence: float
    context: str  # 上下文信息
    file_path: Optional[str] = None
    line_number: Optional[int] = None


class SensitiveDataDetector:
    """敏感数据检测器"""

    def __init__(self, config_file: str = None):
        """
        初始化检测器

        Args:
            config_file: 配置文件路径
        """
        self.logger = self._setup_logger()
        self.patterns = self._load_patterns()
        self.custom_rules = {}

        if config_file and os.path.exists(config_file):
            self._load_config(config_file)

    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger("SensitiveDataDetector")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _load_patterns(self) -> Dict[SensitiveDataType, Dict]:
        """加载预定义的检测模式"""
        patterns = {
            SensitiveDataType.ID_CARD: {
                "pattern": r"\b[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[0-9Xx]\b",
                "validator": self._validate_id_card,
                "confidence": 0.9,
            },
            SensitiveDataType.PHONE: {
                "pattern": r"\b1[3-9]\d{9}\b",
                "validator": self._validate_phone,
                "confidence": 0.8,
            },
            SensitiveDataType.EMAIL: {
                "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                "validator": self._validate_email,
                "confidence": 0.9,
            },
            SensitiveDataType.CREDIT_CARD: {
                "pattern": r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3[0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b",
                "validator": self._validate_credit_card,
                "confidence": 0.95,
            },
            SensitiveDataType.BANK_CARD: {
                "pattern": r"\b[1-9]\d{15,18}\b",
                "validator": self._validate_bank_card,
                "confidence": 0.7,
            },
            SensitiveDataType.IP_ADDRESS: {
                "pattern": r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
                "validator": self._validate_ip,
                "confidence": 0.8,
            },
            SensitiveDataType.MAC_ADDRESS: {
                "pattern": r"\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b",
                "validator": None,
                "confidence": 0.9,
            },
            SensitiveDataType.PASSPORT: {
                "pattern": r"\b[A-Z]\d{8}\b|[A-Z]{2}\d{7}\b",
                "validator": None,
                "confidence": 0.7,
            },
            SensitiveDataType.LICENSE_PLATE: {
                "pattern": r"\b[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z][A-Z][A-Z0-9]{4}[A-Z0-9挂学警港澳]\b",
                "validator": None,
                "confidence": 0.8,
            },
            SensitiveDataType.ORGANIZATION_CODE: {
                "pattern": r"\b[A-Z0-9]{8}-[A-Z0-9]\b",
                "validator": None,
                "confidence": 0.7,
            },
            SensitiveDataType.TAX_NUMBER: {
                "pattern": r"\b\d{15}|\d{17}|\d{20}\b",
                "validator": None,
                "confidence": 0.6,
            },
        }
        return patterns

    def _validate_id_card(self, id_card: str) -> bool:
        """验证身份证号码"""
        if len(id_card) != 18:
            return False

        # 校验位计算
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]

        try:
            sum_val = sum(int(id_card[i]) * weights[i] for i in range(17))
            check_code = check_codes[sum_val % 11]
            return id_card[-1].upper() == check_code
        except (ValueError, IndexError):
            return False

    def _validate_phone(self, phone: str) -> bool:
        """验证手机号码"""
        return len(phone) == 11 and phone.startswith("1")

    def _validate_email(self, email: str) -> bool:
        """验证邮箱地址"""
        return "@" in email and "." in email.split("@")[-1]

    def _validate_credit_card(self, card_number: str) -> bool:
        """使用Luhn算法验证信用卡号"""

        def luhn_check(card_num):
            total = 0
            reverse_digits = card_num[::-1]
            for i, char in enumerate(reverse_digits):
                digit = int(char)
                if i % 2 == 1:
                    digit *= 2
                    if digit > 9:
                        digit -= 9
                total += digit
            return total % 10 == 0

        return luhn_check(card_number.replace(" ", "").replace("-", ""))

    def _validate_bank_card(self, card_number: str) -> bool:
        """验证银行卡号"""
        return 16 <= len(card_number) <= 19

    def _validate_ip(self, ip: str) -> bool:
        """验证IP地址"""
        parts = ip.split(".")
        return all(0 <= int(part) <= 255 for part in parts)

    def _load_config(self, config_file: str):
        """加载配置文件"""
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)

            # 加载自定义规则
            if "custom_rules" in config:
                for rule_name, rule_config in config["custom_rules"].items():
                    self.add_custom_rule(
                        rule_name,
                        rule_config["pattern"],
                        rule_config.get("confidence", 0.5),
                    )

            self.logger.info(f"配置文件加载成功: {config_file}")
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {e}")

    def add_custom_rule(self, name: str, pattern: str, confidence: float = 0.5):
        """添加自定义检测规则"""
        try:
            compiled_pattern = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
            self.custom_rules[name] = {
                "pattern": pattern,
                "compiled": compiled_pattern,
                "confidence": confidence,
            }
            self.logger.info(f"添加自定义规则: {name}")
        except re.error as e:
            self.logger.error(f"无效的正则表达式 {name}: {e}")

    def detect_text(self, text: str, context_length: int = 20) -> List[DetectionResult]:
        """检测文本中的敏感数据"""
        results = []

        # 检测预定义模式
        for data_type, config in self.patterns.items():
            pattern = config["pattern"]
            validator = config.get("validator")
            confidence = config["confidence"]

            for match in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
                value = match.group()
                start, end = match.span()

                # 验证匹配结果
                if validator and not validator(value):
                    continue

                # 获取上下文
                context_start = max(0, start - context_length)
                context_end = min(len(text), end + context_length)
                context = text[context_start:context_end]

                result = DetectionResult(
                    data_type=data_type,
                    value=value,
                    position=(start, end),
                    confidence=confidence,
                    context=context,
                )
                results.append(result)

        # 检测自定义规则
        for rule_name, rule_config in self.custom_rules.items():
            compiled_pattern = rule_config["compiled"]
            confidence = rule_config["confidence"]

            for match in compiled_pattern.finditer(text):
                value = match.group()
                start, end = match.span()

                context_start = max(0, start - context_length)
                context_end = min(len(text), end + context_length)
                context = text[context_start:context_end]

                result = DetectionResult(
                    data_type=SensitiveDataType.CUSTOM,
                    value=value,
                    position=(start, end),
                    confidence=confidence,
                    context=context,
                )
                results.append(result)

        return results

    def detect_file(self, file_path: str) -> List[DetectionResult]:
        """检测文件中的敏感数据"""
        results = []

        try:
            if file_path.endswith(".csv"):
                results.extend(self._detect_csv(file_path))
            elif file_path.endswith((".xlsx", ".xls")):
                results.extend(self._detect_excel(file_path))
            elif file_path.endswith(".json"):
                results.extend(self._detect_json(file_path))
            elif file_path.endswith(".txt"):
                results.extend(self._detect_txt(file_path))
            else:
                self.logger.warning(f"不支持的文件类型: {file_path}")

        except Exception as e:
            self.logger.error(f"检测文件失败 {file_path}: {e}")

        return results

    def _detect_txt(self, file_path: str) -> List[DetectionResult]:
        """检测文本文件"""
        results = []

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_num, line in enumerate(f, 1):
                line_results = self.detect_text(line)
                for result in line_results:
                    result.file_path = file_path
                    result.line_number = line_num
                    results.append(result)

        return results

    def _detect_csv(self, file_path: str) -> List[DetectionResult]:
        """检测CSV文件"""
        results = []

        try:
            df = pd.read_csv(file_path, encoding="utf-8", low_memory=False)

            for row_idx, row in df.iterrows():
                for col_name in df.columns:
                    cell_value = str(row[col_name])
                    if pd.isna(row[col_name]):
                        continue

                    cell_results = self.detect_text(cell_value)
                    for result in cell_results:
                        result.file_path = file_path
                        result.line_number = (
                            row_idx + 2
                        )  # +2 because of header and 0-indexing
                        result.context = (
                            f"列:{col_name}, 行:{row_idx + 2}, 值:{cell_value}"
                        )
                        results.append(result)

        except Exception as e:
            self.logger.error(f"读取CSV文件失败 {file_path}: {e}")

        return results

    def _detect_excel(self, file_path: str) -> List[DetectionResult]:
        """检测Excel文件"""
        results = []

        try:
            excel_file = pd.ExcelFile(file_path)

            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)

                for row_idx, row in df.iterrows():
                    for col_name in df.columns:
                        cell_value = str(row[col_name])
                        if pd.isna(row[col_name]):
                            continue

                        cell_results = self.detect_text(cell_value)
                        for result in cell_results:
                            result.file_path = file_path
                            result.line_number = row_idx + 2
                            result.context = f"工作表:{sheet_name}, 列:{col_name}, 行:{row_idx + 2}, 值:{cell_value}"
                            results.append(result)

        except Exception as e:
            self.logger.error(f"读取Excel文件失败 {file_path}: {e}")

        return results

    def _detect_json(self, file_path: str) -> List[DetectionResult]:
        """检测JSON文件"""
        results = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            def traverse_json(obj, path=""):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        new_path = f"{path}.{key}" if path else key
                        traverse_json(value, new_path)
                elif isinstance(obj, list):
                    for idx, item in enumerate(obj):
                        new_path = f"{path}[{idx}]"
                        traverse_json(item, new_path)
                else:
                    text_value = str(obj)
                    json_results = self.detect_text(text_value)
                    for result in json_results:
                        result.file_path = file_path
                        result.context = f"路径:{path}, 值:{text_value}"
                        results.append(result)

            traverse_json(data)

        except Exception as e:
            self.logger.error(f"读取JSON文件失败 {file_path}: {e}")

        return results

    def detect_directory(
        self, directory_path: str, recursive: bool = True
    ) -> List[DetectionResult]:
        """检测目录中的敏感数据"""
        results = []
        supported_extensions = {".txt", ".csv", ".json", ".xlsx", ".xls"}

        if recursive:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    if any(file.endswith(ext) for ext in supported_extensions):
                        file_path = os.path.join(root, file)
                        results.extend(self.detect_file(file_path))
        else:
            for file in os.listdir(directory_path):
                if any(file.endswith(ext) for ext in supported_extensions):
                    file_path = os.path.join(directory_path, file)
                    if os.path.isfile(file_path):
                        results.extend(self.detect_file(file_path))

        return results

    def generate_report(
        self, results: List[DetectionResult], output_file: str = None
    ) -> Dict:
        """生成检测报告"""
        report = {
            "scan_time": datetime.now().isoformat(),
            "total_findings": len(results),
            "summary": {},
            "details": [],
        }

        # 统计各类型敏感数据数量
        type_counts = {}
        for result in results:
            type_name = result.data_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1

        report["summary"] = type_counts

        # 详细信息
        for result in results:
            detail = {
                "type": result.data_type.value,
                "value_hash": hashlib.md5(result.value.encode()).hexdigest()[
                    :8
                ],  # 只显示哈希值保护隐私
                "position": result.position,
                "confidence": result.confidence,
                "context": (
                    result.context[:100] + "..."
                    if len(result.context) > 100
                    else result.context
                ),
                "file_path": result.file_path,
                "line_number": result.line_number,
            }
            report["details"].append(detail)

        # 保存报告
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            self.logger.info(f"检测报告已保存: {output_file}")

        return report

    def print_results(self, results: List[DetectionResult], show_values: bool = False):
        """打印检测结果"""
        if not results:
            print("未检测到敏感数据")
            return

        print(f"\n检测到 {len(results)} 项敏感数据:")
        print("-" * 80)

        for i, result in enumerate(results, 1):
            print(f"{i}. 类型: {result.data_type.value}")
            if show_values:
                print(f"   值: {result.value}")
            else:
                print(f"   值: {'*' * len(result.value)}")
            print(f"   置信度: {result.confidence:.2f}")
            print(f"   位置: {result.position}")
            if result.file_path:
                print(f"   文件: {result.file_path}")
            if result.line_number:
                print(f"   行号: {result.line_number}")
            print(f"   上下文: {result.context[:100]}...")
            print("-" * 40)


def main():
    """主函数示例"""
    # 创建检测器实例
    detector = SensitiveDataDetector()

    # 添加自定义规则示例
    detector.add_custom_rule("工号模式", r"\b[A-Z]{2}\d{6}\b", confidence=0.8)

    # 测试文本
    test_text = """
    客户信息如下：
    姓名：张三
    身份证：110101199003071234
    手机：13812345678
    邮箱：zhangsan@example.com
    银行卡：6217000010041234567
    """

    print("正在检测文本中的敏感数据...")
    results = detector.detect_text(test_text)
    detector.print_results(results)

    # 生成报告
    report = detector.generate_report(results, "data/sensitive_data_report.json")

    print(f"\n检测摘要:")
    print(f"总计发现: {report['total_findings']} 项敏感数据")
    for data_type, count in report["summary"].items():
        print(f"  {data_type}: {count} 项")


if __name__ == "__main__":
    main()
