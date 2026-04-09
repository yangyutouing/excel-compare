# -*- coding: utf-8 -*-
"""
Excel数据比对与回填工具 - 土豆小助手版
基于Streamlit开发的可爱风格Web应用，支持两个Excel文件的数据比对和字段回填
"""

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import time
import os

# 页面配置 - 土豆主题
st.set_page_config(
    page_title="🥔 土豆数据小助手",
    page_icon="🥔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 自定义CSS样式 - 可爱土豆风格
# ============================================
st.markdown("""
<style>
    /* ===== 整体背景和字体 ===== */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Nunito', 'PingFang SC', 'Microsoft YaHei', sans-serif !important;
    }
    
    /* 背景色 */
    .stApp {
        background: linear-gradient(135deg, #FFF8E7 0%, #FFE4C4 50%, #FFDAB9 100%);
        background-attachment: fixed;
    }
    
    /* 页面主容器 */
    .main .block-container {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(139, 69, 19, 0.1);
    }
    
    /* ===== 标题样式 ===== */
    .potato-header {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
    }
    
    .potato-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #8B4513;
        text-shadow: 2px 2px 4px rgba(139, 69, 19, 0.2);
        margin-bottom: 0.5rem;
        animation: bounce 2s ease-in-out infinite;
    }
    
    .potato-title .emoji {
        font-size: 3rem;
        vertical-align: middle;
        animation: wiggle 1s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    @keyframes wiggle {
        0%, 100% { transform: rotate(-5deg); }
        50% { transform: rotate(5deg); }
    }
    
    .potato-subtitle {
        font-size: 1.1rem;
        color: #D2691E;
        font-weight: 600;
    }
    
    /* ===== 土豆装饰元素 ===== */
    .potato-decoration {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .potato-decoration span {
        font-size: 2rem;
        animation: float 3s ease-in-out infinite;
    }
    
    .potato-decoration span:nth-child(2) { animation-delay: 0.5s; }
    .potato-decoration span:nth-child(3) { animation-delay: 1s; }
    .potato-decoration span:nth-child(4) { animation-delay: 1.5s; }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(5deg); }
    }
    
    /* ===== 卡片样式 ===== */
    .potato-card {
        background: linear-gradient(145deg, #FFFEF9 0%, #FFF5E6 100%);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(139, 69, 19, 0.1);
        border: 2px solid #DEB887;
        transition: all 0.3s ease;
    }
    
    .potato-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(139, 69, 19, 0.15);
    }
    
    .potato-card-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #8B4513;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* ===== 按钮样式 ===== */
    .stButton > button {
        background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(255, 140, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 140, 0, 0.5);
        background: linear-gradient(135deg, #FFB733 0%, #FFA500 100%);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #32CD32 0%, #228B22 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(50, 205, 50, 0.4);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(50, 205, 50, 0.5);
    }
    
    /* ===== 指标卡片 ===== */
    .metric-card {
        background: linear-gradient(145deg, #FFFAF0 0%, #FFE4C4 100%);
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        border: 2px solid #F5DEB3;
        box-shadow: 0 3px 10px rgba(139, 69, 19, 0.1);
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #8B4513;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #D2691E;
    }
    
    /* ===== 进度条样式 ===== */
    .stProgress > div > div {
        background: linear-gradient(90deg, #FFA500, #FFD700, #FFA500);
        border-radius: 20px;
        height: 12px !important;
    }
    
    /* ===== 侧边栏样式 ===== */
    .css-1d391kg {
        background: linear-gradient(180deg, #FFF8DC 0%, #FFE4C4 100%);
    }
    
    .sidebar .stSidebar {
        background: linear-gradient(180deg, #FFF8DC 0%, #FFE4C4 100%);
    }
    
    /* ===== 文件上传区域 ===== */
    .upload-section {
        background: linear-gradient(145deg, #FFFAF0 0%, #FFF5E6 100%);
        border-radius: 20px;
        padding: 1.5rem;
        border: 3px dashed #DEB887;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #FFA500;
        background: linear-gradient(145deg, #FFFFFF 0%, #FFF8DC 100%);
    }
    
    /* ===== 成功/警告/错误提示 ===== */
    .success-cute {
        padding: 1rem 1.5rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #98FB98 0%, #90EE90 100%);
        border: 2px solid #32CD32;
        color: #006400;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .warning-cute {
        padding: 1rem 1.5rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #FFFACD 0%, #FFE4B5 100%);
        border: 2px solid #FFD700;
        color: #8B4513;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .error-cute {
        padding: 1rem 1.5rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #FFB6C1 0%, #FFA0A0 100%);
        border: 2px solid #FF6B6B;
        color: #8B0000;
        font-weight: 600;
    }
    
    /* ===== 标签页样式 ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #FFF5E6;
        border-radius: 16px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        font-weight: 600;
        color: #8B4513;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%) !important;
        color: white !important;
    }
    
    /* ===== 下拉框样式 ===== */
    .stSelectbox > div > div {
        background: #FFFAF0;
        border-radius: 12px;
        border: 2px solid #DEB887;
    }
    
    /* ===== 多选框样式 ===== */
    .stMultiSelect > div > div {
        background: #FFFAF0;
        border-radius: 12px;
        border: 2px solid #DEB887;
    }
    
    /* ===== 分隔线 ===== */
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #DEB887, transparent);
        margin: 1.5rem 0;
    }
    
    /* ===== 展开器样式 ===== */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #FFF8DC 0%, #FFE4C4 100%);
        border-radius: 12px;
        font-weight: 600;
        color: #8B4513;
    }
    
    /* ===== 数据表格样式 ===== */
    .dataframe {
        border-radius: 12px !important;
        overflow: hidden;
    }
    
    .dataframe thead {
        background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%) !important;
        color: white !important;
    }
    
    .dataframe tbody tr:hover {
        background: #FFF8DC !important;
    }
    
    /* ===== 土豆小尾巴动画 ===== */
    .potato-tail {
        display: inline-block;
        animation: tailWag 0.5s ease-in-out infinite;
    }
    
    @keyframes tailWag {
        0%, 100% { transform: rotate(-10deg); }
        50% { transform: rotate(10deg); }
    }
    
    /* ===== 加载动画 ===== */
    .spinner {
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* ===== Footer ===== */
    .footer {
        text-align: center;
        padding: 1rem;
        color: #8B4513;
        font-size: 0.9rem;
    }
    
    .footer-emoji {
        font-size: 1.2rem;
    }
    
    /* ===== 隐藏默认元素 ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* ===== 响应式调整 ===== */
    @media (max-width: 768px) {
        .potato-title {
            font-size: 2rem;
        }
        .potato-subtitle {
            font-size: 0.9rem;
        }
        .metric-value {
            font-size: 1.4rem;
        }
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
            st.info(f"🥔 检测到文件包含 {len(sheet_names)} 个工作表: {', '.join(sheet_names)}")
            selected_sheet = st.selectbox("📋 请选择要使用的工作表", sheet_names)
            df = pd.read_excel(file, sheet_name=selected_sheet, engine='openpyxl')
        
        return df
    except Exception as e:
        st.error(f"❌ 文件加载失败: {str(e)}")
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
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">📝 总行数</div>
            <div class="metric-value">{:,}</div>
        </div>
        """.format(len(df)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">📊 总列数</div>
            <div class="metric-value">{}</div>
        </div>
        """.format(len(df.columns)), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">❓ 空值数量</div>
            <div class="metric-value">{}</div>
        </div>
        """.format(df.isnull().sum().sum()), unsafe_allow_html=True)


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


# ============================================
# 主应用
# ============================================
def main():
    # 土豆装饰头部
    st.markdown("""
    <div class="potato-header">
        <h1 class="potato-title">
            🥔 土豆数据小助手 🥔
        </h1>
        <p class="potato-subtitle">✨ 让数据比对变得像挖土豆一样简单有趣 ✨</p>
    </div>
    
    <div class="potato-decoration">
        <span>🥔</span>
        <span>🍠</span>
        <span>🥔</span>
        <span>🍠</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化session state
    if 'df1' not in st.session_state:
        st.session_state.df1 = None
    if 'df2' not in st.session_state:
        st.session_state.df2 = None
    if 'result_df' not in st.session_state:
        st.session_state.result_df = None
    if 'stats' not in st.session_state:
        st.session_state.stats = None
    
    # 侧边栏 - 土豆使用说明
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <span style="font-size: 3rem;">🥔</span>
            <h2 style="color: #8B4513; margin: 0.5rem 0;">使用说明</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="potato-card" style="margin-bottom: 1rem;">
            <div class="potato-card-header">🌱 操作步骤</div>
            <ol style="color: #8B4513; line-height: 1.8;">
                <li>上传 <b>主表Excel</b> 📁</li>
                <li>上传 <b>数据源Excel</b> 📁</li>
                <li>选择 <b>匹配字段</b> 🔍</li>
                <li>选择 <b>回填字段</b> 🔄</li>
                <li>点击 <b>开始比对</b> 🚀</li>
                <li>下载 <b>结果文件</b> 📥</li>
            </ol>
        </div>
        
        <div class="potato-card">
            <div class="potato-card-header">💡 温馨提示</div>
            <ul style="color: #8B4513; line-height: 1.8;">
                <li>匹配字段需要有对应关系</li>
                <li>只会回填存在的记录</li>
                <li>原始数据不会被修改</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # 土豆尾巴装饰
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <span style="font-size: 1rem;">小土豆正在努力工作中</span>
            <div style="font-size: 2rem; margin-top: 0.5rem;">
                🥔 <span class="potato-tail">🌿</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("🥔 v2.0 可爱版")
    
    # 文件上传区域
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="potato-card">
            <div class="potato-card-header">📁 主表 (文件1)</div>
        </div>
        """, unsafe_allow_html=True)
        
        file1 = st.file_uploader(
            "选择Excel文件作为主表",
            type=['xlsx', 'xls'],
            help="🥔 主表将作为输出文件的基础，数据将被回填到此表",
            label_visibility="collapsed"
        )
        
        if file1:
            with st.spinner("🥔 土豆正在加载文件..."):
                df1 = load_excel_file(file1)
                if df1 is not None:
                    st.session_state.df1 = df1
                    st.markdown("""
                    <div class="success-cute">
                        ✅ 已加载: {} 🥔
                    </div>
                    """.format(file1.name), unsafe_allow_html=True)
                    display_column_preview(df1)
    
    with col2:
        st.markdown("""
        <div class="potato-card">
            <div class="potato-card-header">📁 数据源 (文件2)</div>
        </div>
        """, unsafe_allow_html=True)
        
        file2 = st.file_uploader(
            "选择Excel文件作为数据源",
            type=['xlsx', 'xls'],
            help="🍠 数据源提供要回填的数据",
            label_visibility="collapsed"
        )
        
        if file2:
            with st.spinner("🍠 土豆正在加载文件..."):
                df2 = load_excel_file(file2)
                if df2 is not None:
                    st.session_state.df2 = df2
                    st.markdown("""
                    <div class="success-cute">
                        ✅ 已加载: {} 🍠
                    </div>
                    """.format(file2.name), unsafe_allow_html=True)
                    display_column_preview(df2)
    
    # 数据预览
    if st.session_state.df1 is not None or st.session_state.df2 is not None:
        st.markdown("<hr>", unsafe_allow_html=True)
        
        preview_tab1, preview_tab2 = st.tabs(["📋 主表预览", "📋 数据源预览"])
        
        with preview_tab1:
            if st.session_state.df1 is not None:
                st.dataframe(
                    st.session_state.df1.head(20),
                    use_container_width=True,
                    height=300
                )
            else:
                st.markdown("""
                <div style="text-align: center; padding: 3rem; color: #8B4513;">
                    🥔 请上传主表文件
                </div>
                """, unsafe_allow_html=True)
        
        with preview_tab2:
            if st.session_state.df2 is not None:
                st.dataframe(
                    st.session_state.df2.head(20),
                    use_container_width=True,
                    height=300
                )
            else:
                st.markdown("""
                <div style="text-align: center; padding: 3rem; color: #8B4513;">
                    🍠 请上传数据源文件
                </div>
                """, unsafe_allow_html=True)
    
    # 字段配置区域
    if st.session_state.df1 is not None and st.session_state.df2 is not None:
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="potato-card" style="margin-bottom: 1rem;">
            <div class="potato-card-header">⚙️ 字段配置</div>
        </div>
        """, unsafe_allow_html=True)
        
        config_col1, config_col2, config_col3 = st.columns(3)
        
        with config_col1:
            match_col1 = st.selectbox(
                "🎯 主表匹配字段",
                options=[""] + list(st.session_state.df1.columns),
                index=0,
                help="🥔 选择主表中用于匹配的字段"
            )
        
        with config_col2:
            match_col2 = st.selectbox(
                "🎯 数据源匹配字段",
                options=[""] + list(st.session_state.df2.columns),
                index=0,
                help="🍠 选择数据源中用于匹配的字段"
            )
        
        with config_col3:
            fill_cols = st.multiselect(
                "🔄 回填字段",
                options=list(st.session_state.df2.columns),
                default=[],
                help="✨ 选择要从数据源回填到主表的字段"
            )
        
        # 显示字段预览
        if match_col1 and match_col2:
            st.markdown("<hr>", unsafe_allow_html=True)
            preview_col1, preview_col2 = st.columns(2)
            
            with preview_col1:
                st.markdown(f"**🥔 主表 - `{match_col1}` 字段预览**")
                if match_col1 in st.session_state.df1.columns:
                    unique_count = st.session_state.df1[match_col1].nunique()
                    null_count = st.session_state.df1[match_col1].isnull().sum()
                    st.caption(f"✨ 唯一值: {unique_count:,} | ❓ 空值: {null_count:,}")
                    st.write(st.session_state.df1[match_col1].dropna().head(10).tolist())
            
            with preview_col2:
                st.markdown(f"**🍠 数据源 - `{match_col2}` 字段预览**")
                if match_col2 in st.session_state.df2.columns:
                    unique_count = st.session_state.df2[match_col2].nunique()
                    null_count = st.session_state.df2[match_col2].isnull().sum()
                    st.caption(f"✨ 唯一值: {unique_count:,} | ❓ 空值: {null_count:,}")
                    st.write(st.session_state.df2[match_col2].dropna().head(10).tolist())
        
        # 执行按钮
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # 土豆装饰按钮
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        
        with col_btn2:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 0.5rem;">
                🥔 🍠 🥔 🍠 🥔
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 开始比对与回填", type="primary", use_container_width=True):
                # 验证配置
                if not match_col1:
                    st.markdown("""
                    <div class="error-cute">
                        ❌ 请选择主表匹配字段 🥔
                    </div>
                    """, unsafe_allow_html=True)
                    return
                if not match_col2:
                    st.markdown("""
                    <div class="error-cute">
                        ❌ 请选择数据源匹配字段 🍠
                    </div>
                    """, unsafe_allow_html=True)
                    return
                if not fill_cols:
                    st.markdown("""
                    <div class="error-cute">
                        ❌ 请选择至少一个回填字段 ✨
                    </div>
                    """, unsafe_allow_html=True)
                    return
                
                # 显示进度条
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(progress):
                    progress_bar.progress(progress)
                    status_text.text(f"🥔 土豆正在努力处理... {int(progress * 100)}%")
                
                # 执行比对
                with st.spinner("🍠 正在处理数据..."):
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
                st.markdown("<hr>", unsafe_allow_html=True)
                
                st.markdown("""
                <div class="potato-card" style="margin-bottom: 1rem;">
                    <div class="potato-card-header">📊 处理结果统计</div>
                </div>
                """, unsafe_allow_html=True)
                
                result_col1, result_col2, result_col3, result_col4 = st.columns(4)
                
                with result_col1:
                    st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">📝 总行数</div>
                        <div class="metric-value">{:,}</div>
                    </div>
                    """.format(stats['total_rows']), unsafe_allow_html=True)
                
                with result_col2:
                    st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">✅ 匹配成功</div>
                        <div class="metric-value">{:,}</div>
                    </div>
                    """.format(stats['matched_rows']), unsafe_allow_html=True)
                
                with result_col3:
                    st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">❌ 匹配失败</div>
                        <div class="metric-value">{:,}</div>
                    </div>
                    """.format(stats['unmatched_rows']), unsafe_allow_html=True)
                
                with result_col4:
                    st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">✨ 回填单元格</div>
                        <div class="metric-value">{:,}</div>
                    </div>
                    """.format(stats['filled_cells']), unsafe_allow_html=True)
                
                # 计算匹配率
                match_rate = (stats['matched_rows'] / stats['total_rows'] * 100) if stats['total_rows'] > 0 else 0
                
                # 土豆庆祝动画
                st.markdown("<br>", unsafe_allow_html=True)
                
                if match_rate >= 80:
                    st.markdown(f"""
                    <div class="success-cute" style="font-size: 1.1rem;">
                        🎉 太棒了！比对完成！匹配成功率 <strong>{match_rate:.1f}%</strong> 🥔🎉
                    </div>
                    """, unsafe_allow_html=True)
                elif match_rate >= 50:
                    st.markdown(f"""
                    <div class="warning-cute" style="font-size: 1.1rem;">
                        🤔 比对完成啦！匹配成功率 <strong>{match_rate:.1f}%</strong>，部分土豆还没找到家 🍠
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="warning-cute" style="font-size: 1.1rem;">
                        😅 匹配成功率有点低 (<strong>{match_rate:.1f}%</strong>)，土豆们迷路了... 🥔 请检查匹配字段配置哦！
                    </div>
                    """, unsafe_allow_html=True)
                
                # 土豆装饰
                st.markdown("""
                <div class="potato-decoration" style="margin-top: 1rem;">
                    <span>🥔</span>
                    <span>🍠</span>
                    <span>🥔</span>
                    <span>🍠</span>
                    <span>🥔</span>
                </div>
                """, unsafe_allow_html=True)
                
                # 显示错误信息
                if stats['errors']:
                    with st.expander("🐛 查看错误信息"):
                        for error in stats['errors']:
                            st.markdown(f"""
                            <div class="error-cute">
                                ❌ {error}
                            </div>
                            """, unsafe_allow_html=True)
                
                # 结果预览
                with st.expander("👁️ 预览处理结果"):
                    st.dataframe(
                        result_df.head(50),
                        use_container_width=True,
                        height=400
                    )
                
                # 下载按钮
                st.markdown("<hr>", unsafe_allow_html=True)
                
                # 生成下载文件
                excel_bytes = excel_to_bytes(result_df, "比对结果.xlsx")
                
                download_col1, download_col2, download_col3 = st.columns([1, 1, 1])
                
                with download_col1:
                    st.markdown("""
                    <div style="text-align: center;">
                        <span style="font-size: 2rem;">🥔</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with download_col2:
                    st.download_button(
                        label="📥 下载结果Excel",
                        data=excel_bytes,
                        file_name="Excel比对结果.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        type="primary",
                        use_container_width=True
                    )
                
                with download_col3:
                    st.markdown("""
                    <div style="text-align: center;">
                        <span style="font-size: 2rem;">🍠</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="text-align: center; color: #8B4513; margin-top: 1rem;">
                    ⏱️ 处理耗时: <strong>{stats['processing_time']:.2f}</strong> 秒 | 
                    📊 文件包含 <strong>{len(result_df):,}</strong> 行 × <strong>{len(result_df.columns)}</strong> 列
                </div>
                """, unsafe_allow_html=True)
    
    # 底部土豆装饰
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer">
        <div class="footer-emoji">🥔 🍠 🥔 🍠 🥔</div>
        <p>💡 提示: 请确保Excel文件格式正确，匹配字段内容一致哦~</p>
        <p>Made with 🥔 by 土豆数据小助手</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
