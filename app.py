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
# 自定义CSS样式 - 可爱土豆风格（简化版，修复遮挡问题）
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
    }
    
    /* 页面主容器 */
    .main .block-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(139, 69, 19, 0.1);
    }
    
    /* ===== 标题样式 ===== */
    .potato-header {
        text-align: center;
        padding: 1rem 0 0.5rem 0;
        margin-bottom: 0.5rem;
    }
    
    .potato-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #8B4513;
        margin-bottom: 0.3rem;
    }
    
    .potato-subtitle {
        font-size: 1rem;
        color: #D2691E;
        font-weight: 600;
    }
    
    /* ===== 土豆静态装饰 ===== */
    .potato-decoration {
        text-align: center;
        margin: 0.8rem 0;
        color: #8B4513;
        font-size: 1.5rem;
        letter-spacing: 0.5rem;
    }
    
    /* ===== 卡片样式 ===== */
    .potato-card {
        background: linear-gradient(145deg, #FFFEF9 0%, #FFF5E6 100%);
        border-radius: 16px;
        padding: 1rem 1.2rem;
        box-shadow: 0 2px 10px rgba(139, 69, 19, 0.08);
        border: 2px solid #DEB887;
    }
    
    .potato-card-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #8B4513;
        margin-bottom: 0.8rem;
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
    }
    
    .stButton > button:hover {
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
    }
    
    /* ===== 指标卡片 ===== */
    .metric-card {
        background: linear-gradient(145deg, #FFFAF0 0%, #FFE4C4 100%);
        border-radius: 14px;
        padding: 1rem;
        text-align: center;
        border: 2px solid #F5DEB3;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #8B4513;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    
    .metric-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #D2691E;
    }
    
    /* ===== 进度条样式 ===== */
    .stProgress > div > div {
        background: linear-gradient(90deg, #FFA500, #FFD700);
        border-radius: 20px;
        height: 10px !important;
    }
    
    /* ===== 侧边栏样式 ===== */
    .sidebar .stSidebar {
        background: linear-gradient(180deg, #FFF8DC 0%, #FFE4C4 100%);
    }
    
    /* ===== 成功/警告/错误提示 ===== */
    .success-cute {
        padding: 0.8rem 1.2rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #98FB98 0%, #90EE90 100%);
        border: 2px solid #32CD32;
        color: #006400;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    
    .warning-cute {
        padding: 0.8rem 1.2rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #FFFACD 0%, #FFE4B5 100%);
        border: 2px solid #FFD700;
        color: #8B4513;
        font-weight: 600;
    }
    
    .error-cute {
        padding: 0.8rem 1.2rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #FFB6C1 0%, #FFA0A0 100%);
        border: 2px solid #FF6B6B;
        color: #8B0000;
        font-weight: 600;
    }
    
    /* ===== 标签页样式 ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #FFF5E6;
        border-radius: 14px;
        padding: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        font-weight: 600;
        color: #8B4513;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%) !important;
        color: white !important;
    }
    
    /* ===== 隐藏默认元素 ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* ===== 分隔线 ===== */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #DEB887, transparent);
        margin: 1rem 0;
    }
    
    /* ===== 展开器样式 ===== */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #FFF8DC 0%, #FFE4C4 100%);
        border-radius: 12px;
        font-weight: 600;
        color: #8B4513;
    }
    
    /* ===== Footer ===== */
    .footer {
        text-align: center;
        padding: 0.8rem;
        color: #8B4513;
        font-size: 0.9rem;
    }
    
    /* ===== 响应式调整 ===== */
    @media (max-width: 768px) {
        .potato-title {
            font-size: 1.8rem;
        }
        .metric-value {
            font-size: 1.3rem;
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
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    match_col1: str,
    match_col2: str,
    fill_cols: list,
    progress_callback=None
) -> tuple[pd.DataFrame, dict]:
    """执行数据比对和回填"""
    start_time = time.time()
    
    result_df = df1.copy()
    
    stats = {
        "total_rows": len(df1),
        "matched_rows": 0,
        "filled_cells": 0,
        "unmatched_rows": 0,
        "errors": []
    }
    
    if match_col1 not in df1.columns:
        stats["errors"].append(f"主表缺少匹配字段: {match_col1}")
        return result_df, stats
    
    if match_col2 not in df2.columns:
        stats["errors"].append(f"数据源缺少匹配字段: {match_col2}")
        return result_df, stats
    
    invalid_fill_cols = [col for col in fill_cols if col not in df2.columns]
    if invalid_fill_cols:
        stats["errors"].append(f"数据源缺少回填字段: {', '.join(invalid_fill_cols)}")
        fill_cols = [col for col in fill_cols if col in df2.columns]
    
    if not fill_cols:
        stats["errors"].append("没有有效的回填字段")
        return result_df, stats
    
    source_dict = {}
    for idx, row in df2.iterrows():
        key = row[match_col2]
        if pd.notna(key):
            source_dict[key] = {col: row[col] for col in fill_cols}
    
    total = len(df1)
    for idx, (result_idx, row) in enumerate(result_df.iterrows()):
        match_value = row[match_col1]
        
        if pd.notna(match_value) and match_value in source_dict:
            stats["matched_rows"] += 1
            for col in fill_cols:
                new_value = source_dict[match_value][col]
                if pd.notna(new_value):
                    result_df.at[result_idx, col] = new_value
                    stats["filled_cells"] += 1
        else:
            stats["unmatched_rows"] += 1
        
        if progress_callback and idx % 100 == 0:
            progress = (idx + 1) / total
            progress_callback(progress)
    
    if progress_callback:
        progress_callback(1.0)
    
    stats["processing_time"] = time.time() - start_time
    
    return result_df, stats


# ============================================
# 主应用
# ============================================
def main():
    # 标题区域 - 静态装饰，不使用动画
    st.markdown("""
    <div class="potato-header">
        <h1 class="potato-title">🥔 土豆数据小助手 🥔</h1>
        <p class="potato-subtitle">✨ 让数据工作变得像挖土豆一样简单有趣 ✨</p>
    </div>
    
    <div class="potato-decoration">🥔 🍠 🥔 🍠 🥔</div>
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
        <div style="text-align: center; padding: 0.5rem 0;">
            <span style="font-size: 2.5rem;">🥔</span>
            <h2 style="color: #8B4513; margin: 0.3rem 0;">使用说明</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="potato-card" style="margin-bottom: 0.8rem;">
            <div class="potato-card-header">🌱 操作步骤</div>
            <ol style="color: #8B4513; line-height: 1.8; font-size: 0.9rem; padding-left: 1.2rem;">
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
            <ul style="color: #8B4513; line-height: 1.7; font-size: 0.9rem; padding-left: 1.2rem;">
                <li>匹配字段需要有对应关系</li>
                <li>只会回填存在的记录</li>
                <li>原始数据不会被修改</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem;">
            <span style="font-size: 2rem;">🥔 🌿</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("🥔 v2.0 ")
    
    # 文件上传区域 - 简洁布局
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="potato-card"><div class="potato-card-header">📁 主表（文件1）</div></div>', unsafe_allow_html=True)
        
        file1 = st.file_uploader(
            "点击上传或拖拽文件到此处",
            type=['xlsx', 'xls'],
            help="🥔 主表将作为输出文件的基础",
            key="file_uploader_1"
        )
        
        if file1:
            with st.spinner("🥔 加载中..."):
                df1 = load_excel_file(file1)
                if df1 is not None:
                    st.session_state.df1 = df1
                    st.markdown(f"""
                    <div class="success-cute">
                        ✅ 已加载：{file1.name}
                    </div>
                    """, unsafe_allow_html=True)
                    display_column_preview(df1)
    
    with col2:
        st.markdown('<div class="potato-card"><div class="potato-card-header">📁 数据源（文件2）</div></div>', unsafe_allow_html=True)
        
        file2 = st.file_uploader(
            "点击上传或拖拽文件到此处",
            type=['xlsx', 'xls'],
            help="🍠 数据源提供要回填的数据",
            key="file_uploader_2"
        )
        
        if file2:
            with st.spinner("🍠 加载中..."):
                df2 = load_excel_file(file2)
                if df2 is not None:
                    st.session_state.df2 = df2
                    st.markdown(f"""
                    <div class="success-cute">
                        ✅ 已加载：{file2.name}
                    </div>
                    """, unsafe_allow_html=True)
                    display_column_preview(df2)
    
    # 数据预览
    if st.session_state.df1 is not None or st.session_state.df2 is not None:
        st.markdown("<hr>", unsafe_allow_html=True)
        
        preview_tab1, preview_tab2 = st.tabs(["📋 主表预览", "📋 数据源预览"])
        
        with preview_tab1:
            if st.session_state.df1 is not None:
                st.dataframe(st.session_state.df1.head(20), use_container_width=True, height=280)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 2rem; color: #8B4513;">
                    🥔 请上传主表文件
                </div>
                """, unsafe_allow_html=True)
        
        with preview_tab2:
            if st.session_state.df2 is not None:
                st.dataframe(st.session_state.df2.head(20), use_container_width=True, height=280)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 2rem; color: #8B4513;">
                    🍠 请上传数据源文件
                </div>
                """, unsafe_allow_html=True)
    
    # 字段配置区域
    if st.session_state.df1 is not None and st.session_state.df2 is not None:
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown('<div class="potato-card"><div class="potato-card-header">⚙️ 字段配置</div></div>', unsafe_allow_html=True)
        
        config_col1, config_col2, config_col3 = st.columns(3)
        
        with config_col1:
            match_col1 = st.selectbox(
                "🎯 主表匹配字段",
                options=["（请选择）"] + list(st.session_state.df1.columns),
                index=0,
                help="选择主表中用于匹配的字段"
            )
            if match_col1 == "（请选择）":
                match_col1 = ""
        
        with config_col2:
            match_col2 = st.selectbox(
                "🎯 数据源匹配字段",
                options=["（请选择）"] + list(st.session_state.df2.columns),
                index=0,
                help="选择数据源中用于匹配的字段"
            )
            if match_col2 == "（请选择）":
                match_col2 = ""
        
        with config_col3:
            fill_cols = st.multiselect(
                "🔄 回填字段",
                options=list(st.session_state.df2.columns),
                default=[],
                help="选择要从数据源回填到主表的字段"
            )
        
        # 字段预览
        if match_col1 and match_col2:
            preview_col1, preview_col2 = st.columns(2)
            
            with preview_col1:
                st.markdown(f"**🥔 主表 `{match_col1}` 预览**")
                if match_col1 in st.session_state.df1.columns:
                    unique_count = st.session_state.df1[match_col1].nunique()
                    null_count = st.session_state.df1[match_col1].isnull().sum()
                    st.caption(f"唯一值：{unique_count:,} | 空值：{null_count:,}")
                    st.write(st.session_state.df1[match_col1].dropna().head(8).tolist())
            
            with preview_col2:
                st.markdown(f"**🍠 数据源 `{match_col2}` 预览**")
                if match_col2 in st.session_state.df2.columns:
                    unique_count = st.session_state.df2[match_col2].nunique()
                    null_count = st.session_state.df2[match_col2].isnull().sum()
                    st.caption(f"唯一值：{unique_count:,} | 空值：{null_count:,}")
                    st.write(st.session_state.df2[match_col2].dropna().head(8).tolist())
        
        # 执行按钮
        st.markdown("<hr>", unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        
        with col_btn2:
            if st.button("🚀 开始比对与回填", type="primary", use_container_width=True):
                if not match_col1:
                    st.markdown("""
                    <div class="error-cute">❌ 请选择主表匹配字段 🥔</div>
                    """, unsafe_allow_html=True)
                    return
                if not match_col2:
                    st.markdown("""
                    <div class="error-cute">❌ 请选择数据源匹配字段 🍠</div>
                    """, unsafe_allow_html=True)
                    return
                if not fill_cols:
                    st.markdown("""
                    <div class="error-cute">❌ 请选择至少一个回填字段 ✨</div>
                    """, unsafe_allow_html=True)
                    return
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(progress):
                    progress_bar.progress(progress)
                    status_text.text(f"🥔 处理中... {int(progress * 100)}%")
                
                with st.spinner("🍠 处理数据..."):
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
                
                st.session_state.result_df = result_df
                st.session_state.stats = stats
                
                # 统计结果
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown('<div class="potato-card"><div class="potato-card-header">📊 处理结果统计</div></div>', unsafe_allow_html=True)
                
                result_col1, result_col2, result_col3, result_col4 = st.columns(4)
                
                with result_col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">📝 总行数</div>
                        <div class="metric-value">{stats['total_rows']:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with result_col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">✅ 匹配成功</div>
                        <div class="metric-value">{stats['matched_rows']:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with result_col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">❌ 匹配失败</div>
                        <div class="metric-value">{stats['unmatched_rows']:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with result_col4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">✨ 回填单元格</div>
                        <div class="metric-value">{stats['filled_cells']:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 匹配结果提示
                match_rate = (stats['matched_rows'] / stats['total_rows'] * 100) if stats['total_rows'] > 0 else 0
                
                if match_rate >= 80:
                    st.markdown(f"""
                    <div class="success-cute" style="font-size: 1rem; margin-top: 1rem;">
                        🎉 太棒了！匹配成功率 <strong>{match_rate:.1f}%</strong> 🥔🎉
                    </div>
                    """, unsafe_allow_html=True)
                elif match_rate >= 50:
                    st.markdown(f"""
                    <div class="warning-cute" style="font-size: 1rem; margin-top: 1rem;">
                        🤔 匹配成功率 <strong>{match_rate:.1f}%</strong>，部分土豆还没找到家 🍠
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="warning-cute" style="font-size: 1rem; margin-top: 1rem;">
                        😅 匹配成功率较低 (<strong>{match_rate:.1f}%</strong>)，请检查匹配字段配置 🥔
                    </div>
                    """, unsafe_allow_html=True)
                
                # 土豆装饰
                st.markdown('<div class="potato-decoration" style="margin: 0.8rem 0;">🥔 🍠 🥔 🍠 🥔</div>', unsafe_allow_html=True)
                
                # 错误信息
                if stats['errors']:
                    with st.expander("🐛 查看错误信息"):
                        for error in stats['errors']:
                            st.markdown(f"<div class='error-cute'>❌ {error}</div>", unsafe_allow_html=True)
                
                # 结果预览
                with st.expander("👁️ 预览处理结果"):
                    st.dataframe(result_df.head(50), use_container_width=True, height=380)
                
                # 下载按钮
                st.markdown("<hr>", unsafe_allow_html=True)
                
                excel_bytes = excel_to_bytes(result_df, "比对结果.xlsx")
                
                download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
                
                with download_col1:
                    st.markdown('<span style="font-size: 2rem;">🥔</span>', unsafe_allow_html=True)
                
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
                    st.markdown('<span style="font-size: 2rem;">🍠</span>', unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="text-align: center; color: #8B4513; margin-top: 0.5rem;">
                    ⏱️ 处理耗时：<strong>{stats['processing_time']:.2f}</strong> 秒 | 
                    📊 文件：<strong>{len(result_df):,}</strong> 行 × <strong>{len(result_df.columns)}</strong> 列
                </div>
                """, unsafe_allow_html=True)
    
    # 底部
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer">
        <div style="margin-bottom: 0.3rem;">🥔 🍠 🥔 🍠 🥔</div>
        <p>💡 提示：请确保Excel文件格式正确，匹配字段内容一致</p>
        <p>Made with 🥔 by 洋芋头</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
