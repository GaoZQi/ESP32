import re
import json
import hashlib
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import pandas as pd
import os
from datetime import datetime


class SensitiveDataType(Enum):
    ID_CARD = "身份证号"
    PHONE = "手机号码"
    EMAIL = "邮箱地址"
    CREDIT_CARD = "信用卡号"
    BANK_CARD = "银行卡号"
    IP_ADDRESS = "IP地址"


@dataclass
class DetectionResult:
    data_type: SensitiveDataType
    value: str
    position: Tuple[int, int]
    confidence: float
    context: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None


class SensitiveDataDetector:
    def __init__(self):
        self.logger = self._setup_logger()
        self.patterns = self._load_patterns()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("SensitiveDataDetector")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def _load_patterns(self) -> Dict[SensitiveDataType, Dict]:
        return {
            SensitiveDataType.ID_CARD: {
                'pattern': r'\b[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])'
                           r'(0[1-9]|[12]\d|3[01])\d{3}[0-9Xx]\b',
                'confidence': 0.9
            },
            SensitiveDataType.PHONE: {
                'pattern': r'\b1[3-9]\d{9}\b',
                'confidence': 0.8
            },
            SensitiveDataType.EMAIL: {
                'pattern': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
                'confidence': 0.9
            },
            SensitiveDataType.CREDIT_CARD: {
                'pattern': r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|'
                           r'3[47][0-9]{13}|3[0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b',
                'confidence': 0.95
            },
            SensitiveDataType.BANK_CARD: {
                'pattern': r'\b[1-9]\d{15,18}\b',
                'confidence': 0.7
            },
            SensitiveDataType.IP_ADDRESS: {
                'pattern': r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
                           r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
                'confidence': 0.8
            }
        }

    def detect_text(self, text: str, context_len=20) -> List[DetectionResult]:
        results = []
        for data_type, cfg in self.patterns.items():
            pattern = cfg['pattern']
            confidence = cfg['confidence']
            for match in re.finditer(pattern, text):
                value = match.group()
                start, end = match.span()
                context = text[max(0, start - context_len):min(len(text), end + context_len)]
                results.append(DetectionResult(
                    data_type=data_type,
                    value=value,
                    position=(start, end),
                    confidence=confidence,
                    context=context
                ))
        return results

    def detect_file(self, file_path: str) -> List[DetectionResult]:
        if not os.path.exists(file_path):
            self.logger.error(f"文件不存在: {file_path}")
            return []

        if file_path.endswith(".txt"):
            return self._detect_txt(file_path)
        elif file_path.endswith(".csv"):
            return self._detect_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            return self._detect_excel(file_path)
        else:
            self.logger.warning(f"不支持的文件类型: {file_path}")
            return []

    def _detect_txt(self, path: str) -> List[DetectionResult]:
        results = []
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f, 1):
                for res in self.detect_text(line):
                    res.file_path = path
                    res.line_number = i
                    results.append(res)
        return results

    def _detect_csv(self, path: str) -> List[DetectionResult]:
        results = []
        df = pd.read_csv(path, encoding='utf-8', low_memory=False)
        for row_i, row in df.iterrows():
            for col in df.columns:
                val = str(row[col])
                for res in self.detect_text(val):
                    res.file_path = path
                    res.line_number = row_i + 2
                    res.context = f"{col}: {val}"
                    results.append(res)
        return results

    def _detect_excel(self, path: str) -> List[DetectionResult]:
        results = []
        xls = pd.ExcelFile(path)
        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet)
            for row_i, row in df.iterrows():
                for col in df.columns:
                    val = str(row[col])
                    for res in self.detect_text(val):
                        res.file_path = path
                        res.line_number = row_i + 2
                        res.context = f"{sheet}-{col}: {val}"
                        results.append(res)
        return results

    def summarize(self, results: List[DetectionResult]) -> str:
        if not results:
            return "未检测到敏感数据"

        summary = {}
        for r in results:
            key = r.data_type.value
            summary[key] = summary.get(key, 0) + 1

        lines = [f"共检测到 {len(results)} 项敏感数据："]
        for k, v in summary.items():
            lines.append(f"- {k}: {v} 项")
        return "\n".join(lines)


# 提供给前端：基于文件路径检测
def run_from_path(file_path: str) -> str:
    detector = SensitiveDataDetector()
    results = detector.detect_file(file_path)
    return detector.summarize(results)

