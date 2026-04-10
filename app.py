# -*- coding: utf-8 -*-
"""
🥔 土豆数据工具箱 - 让数据工作变得像挖土豆一样简单有趣
一个可爱风格的Streamlit数据处理工具集
包含：数据比对回填、数据拆分器、数据聚合器等功能
"""

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO, StringIO
import time
import os
import zipfile
from datetime import datetime

# 页面配置 - 土豆主题
st.set_page_config(
    page_title="🥔 土豆数据工具箱",
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
    
    /* ===== 工具卡片样式 ===== */
    .tool-card {
        background: linear-gradient(145deg, #FFFAF0 0%, #FFE4C4 100%);
        border-radius: 16px;
        padding: 1.5rem;
        border: 2px solid #DEB887;
        text-align: center;
        transition: transform 0.2s;
    }
    
    .tool-card:hover {
        transform: translateY(-2px);
    }
    
    .tool-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .tool-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #8B4513;
        margin-bottom: 0.3rem;
    }
    
    .tool-desc {
        font-size: 0.9rem;
        color: #D2691E;
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


# ============================================
# 通用工具函数
# ============================================
def load_excel_file(file) -> pd.DataFrame:
    """加载Excel文件"""
    try:
        excel_file = pd.ExcelFile(file)
        sheet_names = excel_file.sheet_names
        
        if len(sheet_names) == 1:
            df = pd.read_excel(file, engine='openpyxl')
        else:
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
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📝 总行数</div>
            <div class="metric-value">{len(df):,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📊 总列数</div>
            <div class="metric-value">{len(df.columns)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">❓ 空值数量</div>
            <div class="metric-value">{df.isnull().sum().sum()}</div>
        </div>
        """, unsafe_allow_html=True)


def excel_to_bytes(df: pd.DataFrame, filename: str = "result.xlsx") -> bytes:
    """将DataFrame转换为Excel字节流用于下载"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='数据')
    output.seek(0)
    return output.getvalue()


def excel_to_bytes_multi(dfs: list, base_filename: str = "data") -> bytes:
    """将多个DataFrame打包成zip文件"""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for i, df in enumerate(dfs, 1):
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name=f'数据_{i}')
            excel_buffer.seek(0)
            zip_file.writestr(f'{base_filename}_{i:04d}.xlsx', excel_buffer.getvalue())
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


# ============================================
# 页面1：首页
# ============================================
def show_home():
    """显示首页"""
    st.markdown("""
    <div class="potato-header">
        <h1 class="potato-title">🥔 土豆数据工具箱 🥔</h1>
        <p class="potato-subtitle">✨ 让数据工作变得像挖土豆一样简单有趣 ✨</p>
    </div>
    
    <div class="potato-decoration">🥔 🍠 🥔 🍠 🥔</div>
    """, unsafe_allow_html=True)
    
    # 欢迎语
    st.markdown("""
    <div class="potato-card" style="text-align: center; margin: 1rem 0;">
        <p style="font-size: 1.1rem; color: #8B4513; margin: 0;">
            👋 欢迎使用土豆数据工具箱！这里为您准备了各种实用的数据处理工具 🥔
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 工具列表
    st.markdown("""
    <div class="potato-card" style="margin: 1.5rem 0;">
        <div class="potato-card-header">🛠️ 可用工具（点击进入使用）</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 工具1：数据比对回填
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="tool-card" style="padding-bottom: 0.5rem;">
            <div class="tool-icon">🔄</div>
            <div class="tool-title">数据比对回填</div>
            <div class="tool-desc">将两个Excel文件按关键字段进行比对和回填</div>
            <p style="margin-top: 0.5rem; color: #8B4513; font-size: 0.85rem;">
                📁 上传主表和数据源 → 选择匹配字段 → 自动回填
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 进入工具", key="go_compare", use_container_width=True):
            st.session_state.page = "🔄 数据比对回填"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="tool-card" style="padding-bottom: 0.5rem;">
            <div class="tool-icon">✂️</div>
            <div class="tool-title">数据拆分器</div>
            <div class="tool-desc">将大型Excel文件按指定条数拆分成多个文件</div>
            <p style="margin-top: 0.5rem; color: #8B4513; font-size: 0.85rem;">
                📁 上传Excel文件 → 设置拆分条数 → 一键拆分打包
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 进入工具", key="go_split", use_container_width=True):
            st.session_state.page = "✂️ 数据拆分器"
            st.rerun()
    
    # 工具2：数据聚合器
    col3, col4 = st.columns(2, gap="large")
    
    with col3:
        st.markdown("""
        <div class="tool-card" style="padding-bottom: 0.5rem;">
            <div class="tool-icon">🔗</div>
            <div class="tool-title">数据聚合器</div>
            <div class="tool-desc">将相同数据的行合并，让内容聚合更高效</div>
            <p style="margin-top: 0.5rem; color: #8B4513; font-size: 0.85rem;">
                📁 上传Excel文件 → 选择聚合字段 → 一键合并
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 进入工具", key="go_aggregate", use_container_width=True):
            st.session_state.page = "🔗 数据聚合器"
            st.rerun()
    
    with col4:
        st.markdown("""
        <div class="tool-card" style="padding-bottom: 0.5rem; opacity: 0.7;">
            <div class="tool-icon">🚧</div>
            <div class="tool-title">更多工具...</div>
            <div class="tool-desc">更多实用工具正在开发中，敬请期待！</div>
            <p style="margin-top: 0.5rem; color: #8B4513; font-size: 0.85rem;">
                🥔 土豆正在努力种植新的工具...
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.button("🚀 敬请期待", key="go_more", use_container_width=True, disabled=True)
    
    # 版本更新
    st.markdown("""
    <div class="potato-card" style="margin: 1.5rem 0;">
        <div class="potato-card-header">📝 版本更新</div>
        
        
                v2.1当前版本
                1、新增数据聚合器功能
                2、优化数据比对回填逻辑
                3、首页支持点击跳转工具
            
            
                v2.0工具箱版
            
                1、重构为多工具集架构
                2、新增数据拆分器功能
                3、土豆主题UI优化
            
            
                v1.0初始版本
                1、数据比对回填功能
                2、可爱土豆风格界面

    """, unsafe_allow_html=True)
    
    # 底部装饰
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="potato-decoration">🥔 🍠 🥔 🍠 🥔</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer">
        <p>💡 选择上方工具开始使用吧！</p>
        <p>Made with 🥔 by 洋芋头</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# 页面2：数据比对回填
# ============================================
def show_compare_tool():
    """显示数据比对回填工具"""
    st.markdown("""
    <div class="potato-header">
        <h1 class="potato-title">🔄 数据比对回填</h1>
        <p class="potato-subtitle">✨ 将两个Excel文件按关键字段进行数据回填 ✨</p>
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
    
    # 使用说明卡片
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
        st.caption("🥔 数据比对回填")
    
    # 文件上传区域
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
                    st.markdown("""
                    <div class="success-cute">✅ 已加载主表文件</div>
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
                    st.markdown("""
                    <div class="success-cute">✅ 已加载数据源文件</div>
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
        
        # 字段数量对比
        col_count_info = st.columns([1, 2])
        with col_count_info[0]:
            st.markdown(f"""
            <div style="background: #FFF8DC; padding: 1rem; border-radius: 12px;">
                <div style="color: #8B4513; font-size: 0.9rem;">
                    <b>📊 字段数量</b>
                </div>
                <div style="margin-top: 0.5rem; color: #D2691E;">
                    主表：<b>{len(st.session_state.df1.columns)}</b> 个字段<br>
                    数据源：<b>{len(st.session_state.df2.columns)}</b> 个字段
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_count_info[1]:
            st.markdown("""
            <div style="background: #FFE4C4; padding: 1rem; border-radius: 12px;">
                <div style="color: #8B4513; font-size: 0.9rem;">
                    <b>💡 说明</b>
                </div>
                <div style="margin-top: 0.5rem; color: #8B4513; font-size: 0.9rem;">
                    选择<b>匹配字段</b>和<b>回填字段</b>，回填字段会添加到结果表中（带<code>_来源</code>后缀）。
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
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
                options=[col for col in st.session_state.df2.columns],
                default=[],
                help="选择要从数据源回填的字段"
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
            
            # 预估结果字段
            if fill_cols:
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("**📋 结果预估**")
                
                # 计算预估的字段列表
                all_cols1 = list(st.session_state.df1.columns)
                # 回填字段都加_来源后缀
                fill_cols_new = [f"{col}_来源" for col in fill_cols]
                result_cols_count = len(all_cols1) + len(fill_cols_new)
                
                st.markdown(f"""
                <div style="background: #FFF8DC; padding: 1rem; border-radius: 12px; color: #8B4513;">
                    <p style="margin: 0.3rem 0;">• 主表字段：<code>{', '.join(all_cols1)}</code>（{len(all_cols1)}个）</p>
                    <p style="margin: 0.3rem 0;">• 回填字段（加_来源后缀）：<code>{', '.join(fill_cols_new)}</code>（{len(fill_cols_new)}个）</p>
                    <p style="margin: 0.3rem 0;">• <b>结果表总计：{result_cols_count} 个字段</b></p>
                </div>
                """, unsafe_allow_html=True)
        
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
                    <div class="error-cute">❌ 请至少选择一个回填字段 ✨</div>
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
                
                st.markdown('<div class="potato-decoration" style="margin: 0.8rem 0;">🥔 🍠 🥔 🍠 🥔</div>', unsafe_allow_html=True)
                
                # 新增字段提示
                if stats.get('source_cols_added'):
                    added_cols_str = "、".join([f"`{col}`" for col in stats['source_cols_added']])
                    st.markdown(f"""
                    <div class="success-cute" style="margin-bottom: 0.5rem;">
                        📋 已新增数据源字段：{added_cols_str}
                    </div>
                    """, unsafe_allow_html=True)
                
                # 错误信息
                if stats['errors']:
                    with st.expander("🐛 查看提示信息"):
                        for error in stats['errors']:
                            st.markdown(f"<div class='warning-cute'>💡 {error}</div>", unsafe_allow_html=True)
                
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
    st.markdown('<div class="potato-decoration">🥔 🍠 🥔 🍠 🥔</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
        <p>Made with 🥔 by 洋芋头</p>
    </div>
    """, unsafe_allow_html=True)


def compare_and_fill(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    match_col1: str,
    match_col2: str,
    fill_cols: list,
    progress_callback=None
) -> tuple[pd.DataFrame, dict]:
    """执行数据比对，结果包含主表所有字段 + 选中的回填字段（带_来源后缀）"""
    start_time = time.time()
    
    # 复制主表作为结果基础
    result_df = df1.copy()
    
    stats = {
        "total_rows": len(df1),
        "matched_rows": 0,
        "filled_cells": 0,
        "unmatched_rows": 0,
        "source_cols_added": [],
        "errors": []
    }
    
    if match_col1 not in df1.columns:
        stats["errors"].append(f"主表缺少匹配字段: {match_col1}")
        return result_df, stats
    
    if match_col2 not in df2.columns:
        stats["errors"].append(f"数据源缺少匹配字段: {match_col2}")
        return result_df, stats
    
    # 过滤掉无效的回填字段
    valid_fill_cols = [col for col in fill_cols if col in df2.columns]
    if len(valid_fill_cols) != len(fill_cols):
        invalid = [col for col in fill_cols if col not in df2.columns]
        stats["errors"].append(f"数据源缺少字段: {', '.join(invalid)}")
    
    if not valid_fill_cols:
        stats["errors"].append("没有有效的回填字段")
        return result_df, stats
    
    # 为回填字段创建新列名（带_来源后缀）
    new_col_names = []
    for col in valid_fill_cols:
        new_col = f"{col}_来源"
        # 确保新名称不与主表字段冲突
        counter = 1
        while new_col in result_df.columns:
            new_col = f"{col}_来源{counter}"
            counter += 1
        new_col_names.append((col, new_col))
        result_df[new_col] = None  # 预先创建空列
        stats["source_cols_added"].append(new_col)
    
    # 构建数据源字典
    source_dict = {}
    for idx, row in df2.iterrows():
        key = row[match_col2]
        if pd.notna(key):
            source_dict[key] = {orig_col: row[orig_col] for orig_col, _ in new_col_names}
    
    # 执行合并
    total = len(result_df)
    for idx, (result_idx, row) in enumerate(result_df.iterrows()):
        match_value = row[match_col1]
        
        if pd.notna(match_value) and match_value in source_dict:
            stats["matched_rows"] += 1
            for orig_col, new_col in new_col_names:
                source_value = source_dict[match_value][orig_col]
                if pd.notna(source_value):
                    result_df.at[result_idx, new_col] = source_value
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
# 页面3：数据拆分器
# ============================================
def show_split_tool():
    """显示数据拆分器工具"""
    st.markdown("""
    <div class="potato-header">
        <h1 class="potato-title">✂️ 数据拆分器</h1>
        <p class="potato-subtitle">✨ 将大型Excel文件按指定条数拆分成多个文件 ✨</p>
    </div>
    
    <div class="potato-decoration">🥔 🍠 🥔 🍠 🥔</div>
    """, unsafe_allow_html=True)
    
    # 初始化session state
    if 'split_df' not in st.session_state:
        st.session_state.split_df = None
    if 'split_result' not in st.session_state:
        st.session_state.split_result = None
    
    # 使用说明
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
                <li>上传 <b>Excel文件</b> 📁</li>
                <li>输入 <b>拆分条数</b> 🔢</li>
                <li>点击 <b>开始拆分</b> ✂️</li>
                <li>下载 <b>打包文件</b> 📥</li>
            </ol>
        </div>
        
        <div class="potato-card">
            <div class="potato-card-header">💡 温馨提示</div>
            <ul style="color: #8B4513; line-height: 1.7; font-size: 0.9rem; padding-left: 1.2rem;">
                <li>拆分范围：10~100000条</li>
                <li>支持 .xlsx 和 .xls 格式</li>
                <li>结果打包成zip下载</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem;">
            <span style="font-size: 2rem;">🥔 🌿</span>
        </div>
        """, unsafe_allow_html=True)
        st.caption("🥔 数据拆分器")
    
    # 文件上传区域
    st.markdown('<div class="potato-card"><div class="potato-card-header">📁 上传Excel文件</div></div>', unsafe_allow_html=True)
    
    file = st.file_uploader(
        "点击上传或拖拽Excel文件到此处",
        type=['xlsx', 'xls'],
        help="🥔 上传要拆分的Excel文件",
        key="split_file_uploader"
    )
    
    if file:
        with st.spinner("🥔 加载中..."):
            df = load_excel_file(file)
            if df is not None:
                st.session_state.split_df = df
                st.session_state.split_result = None
                st.markdown("""
                <div class="success-cute">✅ 文件加载成功</div>
                """, unsafe_allow_html=True)
                
                # 显示文件信息
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown('<div class="potato-card"><div class="potato-card-header">📊 文件信息</div></div>', unsafe_allow_html=True)
                
                info_col1, info_col2, info_col3 = st.columns(3)
                
                with info_col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">📝 总行数</div>
                        <div class="metric-value">{len(df):,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with info_col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">📊 总列数</div>
                        <div class="metric-value">{len(df.columns)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with info_col3:
                    file_size_mb = file.size / (1024 * 1024)
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">💾 文件大小</div>
                        <div class="metric-value">{file_size_mb:.2f} MB</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 数据预览
                with st.expander("👁️ 预览数据（前20行）"):
                    st.dataframe(df.head(20), use_container_width=True, height=300)
    
    # 拆分配置
    if st.session_state.split_df is not None:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="potato-card"><div class="potato-card-header">⚙️ 拆分配置</div></div>', unsafe_allow_html=True)
        
        config_col1, config_col2 = st.columns([1, 2])
        
        with config_col1:
            split_count = st.number_input(
                "📏 每份条数",
                min_value=10,
                max_value=100000,
                value=1000,
                step=100,
                help="每份文件的行数（10~100000）"
            )
        
        # 计算拆分结果
        total_rows = len(st.session_state.split_df)
        file_count = (total_rows + split_count - 1) // split_count
        
        with config_col2:
            st.markdown(f"""
            <div class="potato-card" style="margin-top: 0.5rem;">
                <div style="display: flex; justify-content: space-around; text-align: center;">
                    <div>
                        <div style="font-size: 0.9rem; color: #8B4513;">📝 原始数据</div>
                        <div style="font-size: 1.3rem; font-weight: 700; color: #D2691E;">{total_rows:,} 条</div>
                    </div>
                    <div style="color: #8B4513; font-size: 1.5rem;">→</div>
                    <div>
                        <div style="font-size: 0.9rem; color: #8B4513;">📁 拆分后</div>
                        <div style="font-size: 1.3rem; font-weight: 700; color: #D2691E;">{file_count} 个文件</div>
                    </div>
                    <div style="color: #8B4513; font-size: 1.5rem;">≈</div>
                    <div>
                        <div style="font-size: 0.9rem; color: #8B4513;">📏 每份约</div>
                        <div style="font-size: 1.3rem; font-weight: 700; color: #D2691E;">~{split_count:,} 条</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 预估拆分详情
        st.markdown("<hr>", unsafe_allow_html=True)
        
        preview_col1, preview_col2 = st.columns(2)
        
        with preview_col1:
            st.markdown("**🥔 拆分预估**")
            st.markdown(f"""
            <div style="background: #FFF8DC; padding: 1rem; border-radius: 12px; color: #8B4513;">
                <p style="margin: 0.3rem 0;">• 预计生成 <strong>{file_count}</strong> 个Excel文件</p>
                <p style="margin: 0.3rem 0;">• 第1个文件：1 ~ {min(split_count, total_rows)} 条</p>
                <p style="margin: 0.3rem 0;">• 最后文件：{(file_count-1)*split_count + 1} ~ {total_rows} 条</p>
                <p style="margin: 0.3rem 0;">• 文件名格式：<code>data_0001.xlsx</code></p>
            </div>
            """, unsafe_allow_html=True)
        
        with preview_col2:
            st.markdown("**🍠 提示**")
            st.markdown("""
            <div style="background: #FFE4C4; padding: 1rem; border-radius: 12px; color: #8B4513;">
                <p style="margin: 0.3rem 0;">💡 数据将被保存为zip压缩包</p>
                <p style="margin: 0.3rem 0;">💡 每个Excel文件包含表头</p>
                <p style="margin: 0.3rem 0;">💡 建议拆分条数不要过大</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 执行拆分按钮
        st.markdown("<hr>", unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        
        with col_btn2:
            if st.button("✂️ 开始拆分", type="primary", use_container_width=True):
                with st.spinner("🍠 正在拆分数据..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # 执行拆分
                    start_time = time.time()
                    split_dfs = []
                    total = len(st.session_state.split_df)
                    
                    for i in range(0, total, split_count):
                        chunk_df = st.session_state.split_df.iloc[i:i + split_count]
                        split_dfs.append(chunk_df)
                        
                        progress = min((i + split_count) / total, 1.0)
                        progress_bar.progress(progress)
                        status_text.text(f"🥔 拆分中... {int(progress * 100)}%")
                    
                    progress_bar.empty()
                    status_text.empty()
                    
                    # 生成zip文件
                    status_text = st.empty()
                    status_text.text("🍠 正在打包文件...")
                    
                    zip_bytes = excel_to_bytes_multi(split_dfs, "data")
                    
                    status_text.empty()
                    processing_time = time.time() - start_time
                    
                    st.session_state.split_result = {
                        'zip_bytes': zip_bytes,
                        'file_count': len(split_dfs),
                        'total_rows': total,
                        'split_count': split_count,
                        'processing_time': processing_time
                    }
                    
                    # 显示成功消息
                    st.markdown("""
                    <div class="success-cute" style="margin-top: 1rem;">
                        🎉 拆分完成！可以下载打包文件了 🥔🎉
                    </div>
                    """, unsafe_allow_html=True)
        
        # 显示下载区域
        if st.session_state.split_result:
            result = st.session_state.split_result
            
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<div class="potato-card"><div class="potato-card-header">📥 下载结果</div></div>', unsafe_allow_html=True)
            
            # 统计信息
            result_col1, result_col2, result_col3, result_col4 = st.columns(4)
            
            with result_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📁 文件数量</div>
                    <div class="metric-value">{result['file_count']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with result_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📝 总行数</div>
                    <div class="metric-value">{result['total_rows']:,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with result_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📏 每份条数</div>
                    <div class="metric-value">{result['split_count']:,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with result_col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">⏱️ 处理耗时</div>
                    <div class="metric-value">{result['processing_time']:.2f}s</div>
                </div>
                """, unsafe_allow_html=True)
            
            # 下载按钮
            download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
            
            with download_col1:
                st.markdown('<span style="font-size: 2rem;">🥔</span>', unsafe_allow_html=True)
            
            with download_col2:
                st.download_button(
                    label="📥 下载ZIP打包文件",
                    data=result['zip_bytes'],
                    file_name=f"拆分数据_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip",
                    type="primary",
                    use_container_width=True
                )
            
            with download_col3:
                st.markdown('<span style="font-size: 2rem;">🍠</span>', unsafe_allow_html=True)
            
            # 文件大小提示
            zip_size_mb = len(result['zip_bytes']) / (1024 * 1024)
            st.markdown(f"""
            <div style="text-align: center; color: #8B4513; margin-top: 0.5rem;">
                📦 打包文件大小：<strong>{zip_size_mb:.2f}</strong> MB
            </div>
            """, unsafe_allow_html=True)
    
    # 底部
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="potato-decoration">🥔 🍠 🥔 🍠 🥔</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
        <p>Made with 🥔 by 洋芋头</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# 页面4：数据聚合器
# ============================================
def show_aggregate_tool():
    """显示数据聚合器工具"""
    st.markdown("""
    <div class="potato-header">
        <h1 class="potato-title">🔗 数据聚合器</h1>
        <p class="potato-subtitle">✨ 将相同数据的行合并，让内容聚合更高效 ✨</p>
    </div>
    
    <div class="potato-decoration">🥔 🍠 🥔 🍠 🥔</div>
    """, unsafe_allow_html=True)
    
    # 初始化session state
    if 'agg_df' not in st.session_state:
        st.session_state.agg_df = None
    if 'agg_result' not in st.session_state:
        st.session_state.agg_result = None
    
    # 使用说明
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
                <li>上传 <b>Excel文件</b> 📁</li>
                <li>选择 <b>聚合字段</b> 🔑</li>
                <li>选择 <b>待合并字段</b> 📝</li>
                <li>设置 <b>分隔符</b> ✂️</li>
                <li>点击 <b>开始聚合</b> 🚀</li>
                <li>下载 <b>结果文件</b> 📥</li>
            </ol>
        </div>
        
        <div class="potato-card">
            <div class="potato-card-header">💡 示例说明</div>
            <ul style="color: #8B4513; line-height: 1.6; font-size: 0.85rem; padding-left: 1.2rem;">
                <li><b>聚合字段：</b>决定哪些行需要合并</li>
                <li><b>待合并字段：</b>内容会被连接起来</li>
                <li><b>分隔符：</b>连接时的分隔符号</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem;">
            <span style="font-size: 2rem;">🥔 🌿</span>
        </div>
        """, unsafe_allow_html=True)
        st.caption("🥔 数据聚合器")
    
    # 文件上传区域
    st.markdown('<div class="potato-card"><div class="potato-card-header">📁 上传Excel文件</div></div>', unsafe_allow_html=True)
    
    file = st.file_uploader(
        "点击上传或拖拽Excel文件到此处",
        type=['xlsx', 'xls'],
        help="🥔 上传要聚合的Excel文件",
        key="agg_file_uploader"
    )
    
    if file:
        with st.spinner("🥔 加载中..."):
            df = load_excel_file(file)
            if df is not None:
                st.session_state.agg_df = df
                st.session_state.agg_result = None
                st.markdown("""
                <div class="success-cute">✅ 文件加载成功</div>
                """, unsafe_allow_html=True)
                
                # 显示文件信息
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown('<div class="potato-card"><div class="potato-card-header">📊 文件信息</div></div>', unsafe_allow_html=True)
                
                info_col1, info_col2, info_col3 = st.columns(3)
                
                with info_col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">📝 总行数</div>
                        <div class="metric-value">{len(df):,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with info_col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">📊 总列数</div>
                        <div class="metric-value">{len(df.columns)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with info_col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">📋 字段列表</div>
                        <div class="metric-value">{len(df.columns)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 显示所有字段
                st.markdown("**📋 可用字段：**")
                fields_display = "、".join([f"`{col}`" for col in df.columns])
                st.markdown(f"<div style='color: #8B4513;'>{fields_display}</div>", unsafe_allow_html=True)
                
                # 数据预览
                with st.expander("👁️ 预览数据（前20行）"):
                    st.dataframe(df.head(20), use_container_width=True, height=300)
    
    # 聚合配置
    if st.session_state.agg_df is not None:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="potato-card"><div class="potato-card-header">⚙️ 聚合配置</div></div>', unsafe_allow_html=True)
        
        # 字段选择
        config_col1, config_col2 = st.columns(2)
        
        with config_col1:
            agg_cols = st.multiselect(
                "🔑 聚合字段（相同值的行会合并）",
                options=list(st.session_state.agg_df.columns),
                default=[],
                help="选择用于分组的字段，这些字段完全相同的行会被合并"
            )
        
        with config_col2:
            merge_cols = st.multiselect(
                "📝 待合并字段（内容会拼接在一起）",
                options=[col for col in st.session_state.agg_df.columns if col not in agg_cols],
                default=[],
                help="选择要合并内容的字段"
            )
        
        # 分隔符设置
        sep_col1, sep_col2, sep_col3 = st.columns([1, 2, 1])
        
        with sep_col1:
            sep_options = {
                "逗号 ,": ",",
                "分号 ;": ";",
                "顿号 、": "、",
                "竖线 |": "|",
                "空格": " ",
                "换行（换行符）": "\n",
                "斜杠 /": "/",
                "自定义": "custom"
            }
            sep_preset = st.selectbox(
                "🔣 预设分隔符",
                options=list(sep_options.keys()),
                index=0
            )
        
        with sep_col2:
            if sep_preset == "自定义":
                separator = st.text_input(
                    "✏️ 自定义分隔符",
                    value=",",
                    max_chars=10,
                    help="输入自定义的分隔符"
                )
            else:
                separator = sep_options[sep_preset]
                st.text_input(
                    "🔣 分隔符预览",
                    value=f"「{separator}」",
                    disabled=True
                )
        
        with sep_col3:
            st.markdown("""
            <div style="padding: 0.8rem; background: #FFF8DC; border-radius: 12px; text-align: center;">
                <div style="color: #8B4513; font-size: 0.85rem;">💡 示例输出</div>
                <div style="color: #D2691E; font-weight: 600; margin-top: 0.3rem;">
                    A{sep}B{sep}C
                </div>
            </div>
            """.format(sep=separator if separator != "\n" else "换行"), unsafe_allow_html=True)
        
        # 配置验证提示
        if len(agg_cols) == 0 and len(merge_cols) == 0:
            st.markdown("""
            <div class="warning-cute" style="margin-top: 1rem;">
                🤔 请至少选择一个「聚合字段」和一个「待合并字段」来配置聚合规则 🥔
            </div>
            """, unsafe_allow_html=True)
        elif len(agg_cols) == 0:
            st.markdown("""
            <div class="warning-cute" style="margin-top: 1rem;">
                🤔 请至少选择一个「聚合字段」🥔
            </div>
            """, unsafe_allow_html=True)
        elif len(merge_cols) == 0:
            st.markdown("""
            <div class="warning-cute" style="margin-top: 1rem;">
                🤔 请至少选择一个「待合并字段」🍠
            </div>
            """, unsafe_allow_html=True)
        else:
            # 预估聚合结果
            st.markdown("<hr>", unsafe_allow_html=True)
            
            preview_col1, preview_col2 = st.columns(2)
            
            with preview_col1:
                # 计算预估结果
                original_count = len(st.session_state.agg_df)
                
                # 估算聚合后的行数（基于聚合字段的唯一组合数）
                if agg_cols:
                    unique_groups = st.session_state.agg_df.groupby(agg_cols).ngroups
                else:
                    unique_groups = 1
                
                st.markdown("**🥔 聚合预估**")
                st.markdown(f"""
                <div style="background: #FFF8DC; padding: 1rem; border-radius: 12px; color: #8B4513;">
                    <p style="margin: 0.3rem 0;">• 原始数据：<strong>{original_count:,}</strong> 条</p>
                    <p style="margin: 0.3rem 0;">• 聚合后预计：<strong>{unique_groups:,}</strong> 条</p>
                    <p style="margin: 0.3rem 0;">• 减少：<strong>{original_count - unique_groups:,}</strong> 条（{(1 - unique_groups/original_count)*100:.1f}%）</p>
                    <p style="margin: 0.3rem 0;">• 分隔符：<code>{separator if separator != chr(10) else '换行符'}</code></p>
                </div>
                """, unsafe_allow_html=True)
            
            with preview_col2:
                st.markdown("**🍠 提示**")
                st.markdown("""
                <div style="background: #FFE4C4; padding: 1rem; border-radius: 12px; color: #8B4513;">
                    <p style="margin: 0.3rem 0;">💡 聚合字段完全相同的行会被合并</p>
                    <p style="margin: 0.3rem 0;">💡 待合并字段的内容会按顺序拼接</p>
                    <p style="margin: 0.3rem 0;">💡 空值会自动跳过</p>
                    <p style="margin: 0.3rem 0;">💡 非待合并字段保留第一行值</p>
                </div>
                """, unsafe_allow_html=True)
        
        # 执行聚合按钮
        st.markdown("<hr>", unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        
        with col_btn2:
            if st.button("🚀 开始聚合", type="primary", use_container_width=True):
                if len(agg_cols) == 0:
                    st.markdown("""
                    <div class="error-cute">❌ 请至少选择一个「聚合字段」🥔</div>
                    """, unsafe_allow_html=True)
                    return
                
                if len(merge_cols) == 0:
                    st.markdown("""
                    <div class="error-cute">❌ 请至少选择一个「待合并字段」🍠</div>
                    """, unsafe_allow_html=True)
                    return
                
                with st.spinner("🍠 正在聚合数据..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        # 执行聚合
                        start_time = time.time()
                        
                        status_text.text("🥔 正在分析数据结构...")
                        progress_bar.progress(0.2)
                        
                        df = st.session_state.agg_df.copy()
                        
                        # 确定需要保留的字段（非聚合且非待合并的字段）
                        other_cols = [col for col in df.columns if col not in agg_cols and col not in merge_cols]
                        
                        # 构建聚合函数
                        # - 聚合字段：保留（自然保留）
                        # - 待合并字段：用分隔符连接
                        # - 其他字段：取第一个值
                        agg_funcs = {}
                        for col in merge_cols:
                            agg_funcs[col] = lambda x, sep=separator: sep.join(
                                [str(v) for v in x.dropna().astype(str) if str(v).strip()]
                            )
                        for col in other_cols:
                            agg_funcs[col] = 'first'
                        
                        progress_bar.progress(0.4)
                        status_text.text("🥔 正在分组聚合...")
                        
                        # 执行groupby聚合
                        result_df = df.groupby(agg_cols, as_index=False, sort=False).agg(agg_funcs)
                        
                        progress_bar.progress(0.8)
                        status_text.text("🍠 正在整理结果...")
                        
                        # 调整列顺序：聚合字段 + 待合并字段 + 其他字段
                        final_columns = agg_cols + merge_cols + other_cols
                        result_df = result_df[[col for col in final_columns if col in result_df.columns]]
                        
                        progress_bar.progress(1.0)
                        status_text.empty()
                        progress_bar.empty()
                        
                        processing_time = time.time() - start_time
                        
                        st.session_state.agg_result = {
                            'result_df': result_df,
                            'original_count': len(st.session_state.agg_df),
                            'result_count': len(result_df),
                            'processing_time': processing_time
                        }
                        
                        # 显示成功消息
                        st.markdown("""
                        <div class="success-cute" style="margin-top: 1rem;">
                            🎉 聚合完成！可以下载结果文件了 🥔🎉
                        </div>
                        """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        progress_bar.empty()
                        status_text.empty()
                        st.markdown(f"""
                        <div class="error-cute">
                            ❌ 聚合失败：{str(e)} 🥔
                        </div>
                        """, unsafe_allow_html=True)
    
    # 显示聚合结果
    if st.session_state.agg_result:
        result = st.session_state.agg_result
        result_df = result['result_df']
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="potato-card"><div class="potato-card-header">📊 聚合结果统计</div></div>', unsafe_allow_html=True)
        
        # 统计卡片
        result_col1, result_col2, result_col3, result_col4, result_col5 = st.columns(5)
        
        with result_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📝 原始行数</div>
                <div class="metric-value">{result['original_count']:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with result_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📝 聚合后</div>
                <div class="metric-value">{result['result_count']:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with result_col3:
            reduced = result['original_count'] - result['result_count']
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📉 减少行数</div>
                <div class="metric-value">{reduced:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with result_col4:
            reduce_rate = (1 - result['result_count'] / result['original_count']) * 100
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📊 压缩率</div>
                <div class="metric-value">{reduce_rate:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with result_col5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">⏱️ 处理时间</div>
                <div class="metric-value">{result['processing_time']:.2f}s</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 聚合效果提示
        if reduce_rate > 50:
            st.markdown(f"""
            <div class="success-cute" style="margin-top: 1rem;">
                🎉 太棒了！数据压缩了 <strong>{reduce_rate:.1f}%</strong>，效率大幅提升 🥔🎉
            </div>
            """, unsafe_allow_html=True)
        elif reduce_rate > 20:
            st.markdown(f"""
            <div class="success-cute" style="margin-top: 1rem;">
                😊 不错的效果！数据压缩了 <strong>{reduce_rate:.1f}%</strong> 🍠
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="warning-cute" style="margin-top: 1rem;">
                🤔 数据相似度较低，压缩了 <strong>{reduce_rate:.1f}%</strong> 🥔
            </div>
            """, unsafe_allow_html=True)
        
        # 结果预览
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="potato-card"><div class="potato-card-header">👁️ 结果预览</div></div>', unsafe_allow_html=True)
        
        # 预览前50行
        preview_rows = min(50, len(result_df))
        st.dataframe(result_df.head(preview_rows), use_container_width=True, height=350)
        
        st.caption(f"显示前 {preview_rows} 行，共 {len(result_df):,} 行")
        
        # 下载按钮
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="potato-card"><div class="potato-card-header">📥 下载结果</div></div>', unsafe_allow_html=True)
        
        excel_bytes = excel_to_bytes(result_df, "聚合结果.xlsx")
        
        download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
        
        with download_col1:
            st.markdown('<span style="font-size: 2rem;">🥔</span>', unsafe_allow_html=True)
        
        with download_col2:
            st.download_button(
                label="📥 下载聚合结果Excel",
                data=excel_bytes,
                file_name=f"数据聚合结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
                use_container_width=True
            )
        
        with download_col3:
            st.markdown('<span style="font-size: 2rem;">🍠</span>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align: center; color: #8B4513; margin-top: 0.5rem;">
            📊 结果：<strong>{len(result_df):,}</strong> 行 × <strong>{len(result_df.columns)}</strong> 列
        </div>
        """, unsafe_allow_html=True)
    
    # 底部
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="potato-decoration">🥔 🍠 🥔 🍠 🥔</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
        <p>Made with 🥔 by 洋芋头</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# 主应用入口
# ============================================
def main():
    """主应用入口"""
    # 侧边栏导航
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
            <span style="font-size: 3rem;">🥔</span>
            <h1 style="color: #8B4513; margin: 0.3rem 0; font-size: 1.3rem;">土豆数据工具箱</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # 工具选项列表
        options = ["🏠 首页", "🔄 数据比对回填", "✂️ 数据拆分器", "🔗 数据聚合器"]
        
        # 初始化或读取当前页面
        if 'page' not in st.session_state:
            st.session_state.page = options[0]
        
        # 根据 session_state 设置默认选中
        try:
            default_index = options.index(st.session_state.page)
        except ValueError:
            default_index = 0
        
        # 注意：不使用 key 参数，让 index 参数根据 session_state.page 生效
        page = st.radio(
            "🧭 选择工具",
            options=options,
            index=default_index,
            label_visibility="collapsed"
        )
        
        # 更新 session_state
        st.session_state.page = page
        
        st.divider()
        
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem;">
            <span style="font-size: 1.5rem;">🥔 🍠 🥔</span>
            <p style="color: #8B4513; font-size: 0.85rem; margin: 0.3rem 0;">v2.1 工具箱版</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 根据选择显示对应页面
    if page == "🏠 首页":
        show_home()
    elif page == "🔄 数据比对回填":
        show_compare_tool()
    elif page == "✂️ 数据拆分器":
        show_split_tool()
    elif page == "🔗 数据聚合器":
        show_aggregate_tool()


if __name__ == "__main__":
    main()
