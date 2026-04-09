# -*- coding: utf-8 -*-
"""
Excel数据比对与回填工具
基于Streamlit开发的Web应用，支持两个Excel文件的数据比对和字段回填
"""

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import time
import os

# 页面配置
st.set_page_config(
    page_title="Excel数据比对工具",
    page_icon="📊",
    layout="wide"
)

# 自定义样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)


def load_excel_file(file) -> pd.DataFrame:
    """加载Excel文件"""
    try:
        # 获取sheet名称
        excel_file = pd.ExcelFile(file)
        sheet_names = excel_file.sheet_names
        
        if len(sheet_names) == 1:
            df = pd.read_excel(file, engine='openpyxl')
        else:
            # 如果有多个sheet，显示选择框
            st.info(f"检测到文件包含 {len(sheet_names)} 个工作表: {', '.join(sheet_names)}")
            selected_sheet = st.selectbox("请选择要使用的工作表", sheet_names)
            df = pd.read_excel(file, sheet_name=selected_sheet, engine='openpyxl')
        
        return df
    except Exception as e:
        st.error(f"文件加载失败: {str(e)}")
        return None


def get_column_info(df: pd.DataFrame) -> dict:
    """获取列的基本信息"""
    info = {
        "total_rows": len(df),
        "total_cols": len(df.columns),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "null_counts": df.isnull().sum().to_dict()
    }
    return info


def display_column_preview(df: pd.DataFrame):
    """显示列预览信息"""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("总行数", f"{len(df):,}")
    with col2:
        st.metric("总列数", len(df.columns))
    with col3:
        st.metric("空值数量", df.isnull().sum().sum())


def excel_to_bytes(df: pd.DataFrame, filename: str = "result.xlsx") -> bytes:
    """将DataFrame转换为Excel字节流用于下载"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='比对结果')
    
    output.seek(0)
    return output.getvalue()


def compare_and_fill(
    df1: pd.DataFrame,  # 主表
    df2: pd.DataFrame,  # 数据源
    match_col1: str,    # 主表匹配字段
    match_col2: str,    # 数据源匹配字段
    fill_cols: list,    # 要回填的字段列表
    progress_callback=None
) -> tuple[pd.DataFrame, dict]:
    """
    执行数据比对和回填
    
    Args:
        df1: 主表DataFrame
        df2: 数据源DataFrame
        match_col1: 主表匹配字段
        match_col2: 数据源匹配字段
        fill_cols: 要回填的字段列表
        progress_callback: 进度回调函数
    
    Returns:
        tuple: (处理后的DataFrame, 统计信息字典)
    """
    start_time = time.time()
    
    # 创建结果DataFrame的副本
    result_df = df1.copy()
    
    # 初始化统计信息
    stats = {
        "total_rows": len(df1),
        "matched_rows": 0,
        "filled_cells": 0,
        "unmatched_rows": 0,
        "errors": []
    }
    
    # 确保匹配字段存在
    if match_col1 not in df1.columns:
        stats["errors"].append(f"主表缺少匹配字段: {match_col1}")
        return result_df, stats
    
    if match_col2 not in df2.columns:
        stats["errors"].append(f"数据源缺少匹配字段: {match_col2}")
        return result_df, stats
    
    # 验证回填字段
    invalid_fill_cols = [col for col in fill_cols if col not in df2.columns]
    if invalid_fill_cols:
        stats["errors"].append(f"数据源缺少回填字段: {', '.join(invalid_fill_cols)}")
        fill_cols = [col for col in fill_cols if col in df2.columns]
    
    if not fill_cols:
        stats["errors"].append("没有有效的回填字段")
        return result_df, stats
    
    # 构建数据源字典 (使用match_col2作为键)
    source_dict = {}
    for idx, row in df2.iterrows():
        key = row[match_col2]
        if pd.notna(key):
            source_dict[key] = {col: row[col] for col in fill_cols}
    
    # 执行回填
    total = len(df1)
    for idx, (result_idx, row) in enumerate(result_df.iterrows()):
        match_value = row[match_col1]
        
        if pd.notna(match_value) and match_value in source_dict:
            stats["matched_rows"] += 1
            
            # 回填数据
            for col in fill_cols:
                new_value = source_dict[match_value][col]
                if pd.notna(new_value):
                    result_df.at[result_idx, col] = new_value
                    stats["filled_cells"] += 1
        else:
            stats["unmatched_rows"] += 1
        
        # 更新进度
        if progress_callback and idx % 100 == 0:
            progress = (idx + 1) / total
            progress_callback(progress)
    
    # 最终进度
    if progress_callback:
        progress_callback(1.0)
    
    stats["processing_time"] = time.time() - start_time
    
    return result_df, stats


# 主应用
def main():
    st.markdown('<h1 class="main-header">📊 Excel 数据比对与回填工具</h1>', unsafe_allow_html=True)
    
    # 初始化session state
    if 'df1' not in st.session_state:
        st.session_state.df1 = None
    if 'df2' not in st.session_state:
        st.session_state.df2 = None
    if 'result_df' not in st.session_state:
        st.session_state.result_df = None
    if 'stats' not in st.session_state:
        st.session_state.stats = None
    
    # 侧边栏 - 使用说明
    with st.sidebar:
        st.header("📖 使用说明")
        st.markdown("""
        **操作步骤：**
        1. 上传**主表Excel**（文件1）
        2. 上传**数据源Excel**（文件2）
        3. 选择**匹配字段**（两个表用于匹配的字段）
        4. 选择**回填字段**（从数据源回填到主表的字段）
        5. 点击**开始比对**按钮
        6. 下载**处理结果**
        
        **注意事项：**
        - 两个文件的匹配字段值需要有对应关系
        - 只会回填数据源中存在的记录
        - 原始主表数据不会被修改
        """)
        
        st.divider()
        st.caption("v1.0.0")
    
    # 文件上传区域
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 主表 (文件1)")
        file1 = st.file_uploader(
            "选择Excel文件作为主表",
            type=['xlsx', 'xls'],
            help="主表将作为输出文件的基础，数据将被回填到此表"
        )
        
        if file1:
            with st.spinner("加载文件..."):
                df1 = load_excel_file(file1)
                if df1 is not None:
                    st.session_state.df1 = df1
                    st.success(f"✅ 已加载: {file1.name}")
                    display_column_preview(df1)
    
    with col2:
        st.subheader("📁 数据源 (文件2)")
        file2 = st.file_uploader(
            "选择Excel文件作为数据源",
            type=['xlsx', 'xls'],
            help="数据源提供要回填的数据"
        )
        
        if file2:
            with st.spinner("加载文件..."):
                df2 = load_excel_file(file2)
                if df2 is not None:
                    st.session_state.df2 = df2
                    st.success(f"✅ 已加载: {file2.name}")
                    display_column_preview(df2)
    
    # 数据预览
    if st.session_state.df1 is not None or st.session_state.df2 is not None:
        st.divider()
        
        preview_tab1, preview_tab2 = st.tabs(["主表预览", "数据源预览"])
        
        with preview_tab1:
            if st.session_state.df1 is not None:
                st.dataframe(
                    st.session_state.df1.head(20),
                    use_container_width=True,
                    height=300
                )
            else:
                st.info("请上传主表文件")
        
        with preview_tab2:
            if st.session_state.df2 is not None:
                st.dataframe(
                    st.session_state.df2.head(20),
                    use_container_width=True,
                    height=300
                )
            else:
                st.info("请上传数据源文件")
    
    # 字段配置区域
    if st.session_state.df1 is not None and st.session_state.df2 is not None:
        st.divider()
        st.subheader("⚙️ 字段配置")
        
        config_col1, config_col2, config_col3 = st.columns(3)
        
        with config_col1:
            match_col1 = st.selectbox(
                "主表匹配字段",
                options=[""] + list(st.session_state.df1.columns),
                index=0,
                help="选择主表中用于匹配的字段"
            )
        
        with config_col2:
            match_col2 = st.selectbox(
                "数据源匹配字段",
                options=[""] + list(st.session_state.df2.columns),
                index=0,
                help="选择数据源中用于匹配的字段"
            )
        
        with config_col3:
            fill_cols = st.multiselect(
                "回填字段",
                options=list(st.session_state.df2.columns),
                default=[],
                help="选择要从数据源回填到主表的字段"
            )
        
        # 显示字段预览
        if match_col1 and match_col2:
            st.divider()
            preview_col1, preview_col2 = st.columns(2)
            
            with preview_col1:
                st.markdown(f"**主表 - {match_col1} 字段预览**")
                if match_col1 in st.session_state.df1.columns:
                    unique_count = st.session_state.df1[match_col1].nunique()
                    null_count = st.session_state.df1[match_col1].isnull().sum()
                    st.caption(f"唯一值数量: {unique_count:,} | 空值数量: {null_count:,}")
                    st.write(st.session_state.df1[match_col1].dropna().head(10).tolist())
            
            with preview_col2:
                st.markdown(f"**数据源 - {match_col2} 字段预览**")
                if match_col2 in st.session_state.df2.columns:
                    unique_count = st.session_state.df2[match_col2].nunique()
                    null_count = st.session_state.df2[match_col2].isnull().sum()
                    st.caption(f"唯一值数量: {unique_count:,} | 空值数量: {null_count:,}")
                    st.write(st.session_state.df2[match_col2].dropna().head(10).tolist())
        
        # 执行按钮
        st.divider()
        
        if st.button("🚀 开始比对与回填", type="primary", use_container_width=True):
            # 验证配置
            if not match_col1:
                st.error("请选择主表匹配字段")
                return
            if not match_col2:
                st.error("请选择数据源匹配字段")
                return
            if not fill_cols:
                st.error("请选择至少一个回填字段")
                return
            
            # 显示进度条
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def update_progress(progress):
                progress_bar.progress(progress)
                status_text.text(f"处理进度: {int(progress * 100)}%")
            
            # 执行比对
            with st.spinner("正在处理数据..."):
                result_df, stats = compare_and_fill(
                    st.session_state.df1,
                    st.session_state.df2,
                    match_col1,
                    match_col2,
                    fill_cols,
                    update_progress
                )
            
            progress_bar.empty()
            status_text.empty()
            
            # 保存结果
            st.session_state.result_df = result_df
            st.session_state.stats = stats
            
            # 显示统计结果
            st.divider()
            st.subheader("📊 处理结果统计")
            
            result_col1, result_col2, result_col3, result_col4 = st.columns(4)
            
            with result_col1:
                st.metric("总行数", f"{stats['total_rows']:,}")
            with result_col2:
                st.metric("匹配成功", f"{stats['matched_rows']:,}")
            with result_col3:
                st.metric("匹配失败", f"{stats['unmatched_rows']:,}")
            with result_col4:
                st.metric("回填单元格", f"{stats['filled_cells']:,}")
            
            # 计算匹配率
            match_rate = (stats['matched_rows'] / stats['total_rows'] * 100) if stats['total_rows'] > 0 else 0
            
            if match_rate >= 80:
                st.markdown(f"""
                <div class="success-box">
                ✅ 比对完成！匹配成功率为 <strong>{match_rate:.1f}%</strong>
                </div>
                """, unsafe_allow_html=True)
            elif match_rate >= 50:
                st.markdown(f"""
                <div class="warning-box">
                ⚠️ 比对完成，匹配成功率为 <strong>{match_rate:.1f}%</strong>，部分数据未能匹配
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="warning-box">
                ⚠️ 匹配成功率较低 (<strong>{match_rate:.1f}%</strong>)，请检查匹配字段配置是否正确
                </div>
                """, unsafe_allow_html=True)
            
            # 显示错误信息
            if stats['errors']:
                with st.expander("查看错误信息"):
                    for error in stats['errors']:
                        st.error(error)
            
            # 结果预览
            with st.expander("👁️ 预览处理结果"):
                st.dataframe(
                    result_df.head(50),
                    use_container_width=True,
                    height=400
                )
            
            # 下载按钮
            st.divider()
            
            # 生成下载文件
            excel_bytes = excel_to_bytes(result_df, "比对结果.xlsx")
            
            download_col1, download_col2 = st.columns([1, 2])
            
            with download_col1:
                st.download_button(
                    label="📥 下载结果Excel",
                    data=excel_bytes,
                    file_name="Excel比对结果.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary",
                    use_container_width=True
                )
            
            with download_col2:
                st.caption(f"处理耗时: {stats['processing_time']:.2f} 秒")
                st.caption(f"文件包含 {len(result_df):,} 行 × {len(result_df.columns)} 列")
    
    # 底部提示
    st.divider()
    st.markdown(
        "<p style='text-align: center; color: gray;'>"
        "💡 提示: 请确保Excel文件格式正确，匹配字段内容一致"
        "</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
