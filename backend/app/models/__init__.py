from .medicine import Base as MedicineBase

# 一つにまとめる（重複定義されていない場合）
Base = MedicineBase  # か、統合Baseを定義して共通化
