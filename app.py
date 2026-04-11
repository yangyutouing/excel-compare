# -*- coding: utf-8 -*-
"""
🥔 土豆数据工具箱 - 让数据工作变得像挖土豆一样简单有趣
一个可爱风格的Streamlit数据处理工具集
包含：数据比对回填、数据拆分器、数据聚合器等功能
"""

import streamlit as st
import pandas as pd
import numpy as np
import ipaddress
from io import BytesIO, StringIO
import time
import os
import zipfile
from datetime import datetime
import re
from urllib.parse import urlparse

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
        position: relative;
        z-index: 1;
    }
    
    .potato-decoration span {
        font-size: 2rem;
        animation: float 3s ease-in-out infinite;
        position: relative;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-8px) rotate(3deg); }
    }
    
    /* ===== 卡片样式 ===== */
    .potato-card {
        background: linear-gradient(145deg, #FFFEF9 0%, #FFF5E6 100%);
        border-radius: 20px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 4px 15px rgba(139, 69, 19, 0.1);
        border: 2px solid #DEB887;
        transition: box-shadow 0.3s ease;
        margin-bottom: 0.5rem;
    }
    
    .potato-card:hover {
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
    .stSidebar {
        background: linear-gradient(180deg, #FFF8DC 0%, #FFE4C4 100%);
    }
    
    /* ===== 文件上传区域 ===== */
    .stFileUploader {
        position: relative;
        z-index: 10;
    }
    
    .stFileUploader button {
        z-index: 100 !important;
        position: relative !important;
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
    
    /* ===== 分隔线 ===== */
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #DEB887, transparent);
        margin: 1.5rem 0;
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


# ============================================
# 通用工具函数
# ============================================
def load_csv_file(file) -> pd.DataFrame:
    """加载CSV文件，自动检测编码"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'utf-8-sig']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file, encoding=encoding)
            if len(df.columns) > 0:
                return df
        except (UnicodeDecodeError, Exception):
            file.seek(0)
            continue
    
    # 如果所有编码都失败，尝试用 errors='replace'
    file.seek(0)
    try:
        return pd.read_csv(file, encoding='utf-8', errors='replace')
    except Exception as e:
        st.error(f"❌ CSV文件加载失败: {str(e)}")
        return None


def load_excel_file(file) -> pd.DataFrame:
    """统一加载Excel文件"""
    try:
        return pd.read_excel(file, engine='openpyxl', dtype=str)
    except Exception as e:
        st.error(f"❌ Excel文件加载失败: {str(e)}")
        return None


def load_data_file(file) -> pd.DataFrame:
    """统一加载Excel和CSV文件"""
    file_name = file.name.lower()
    
    if file_name.endswith(('.xlsx', '.xls')):
        return load_excel_file(file)
    elif file_name.endswith('.csv'):
        return load_csv_file(file)
    else:
        st.error(f"❌ 不支持的文件格式: {file_name}")
        return None


def csv_to_bytes(df: pd.DataFrame) -> bytes:
    """将DataFrame转换为CSV字节流用于下载"""
    output = StringIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    output.seek(0)
    return output.getvalue()


def excel_to_bytes(df: pd.DataFrame) -> bytes:
    """将DataFrame转换为Excel字节流用于下载"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='数据')
    output.seek(0)
    return output.getvalue()


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
        empty_count = df.apply(lambda x: x == "").sum().sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">❓ 空值数量</div>
            <div class="metric-value">{empty_count:,}</div>
        </div>
        """, unsafe_allow_html=True)


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
        <h1 class="potato-title">🥔 土豆数据小助手 🥔</h1>
        <p class="potato-subtitle">✨ 让数据工作变得像挖土豆一样简单有趣 ✨</p>
    </div>
    
    <div class="potato-decoration">
        <span>🥔</span>
        <span>🍠</span>
        <span>🥔</span>
        <span>🍠</span>
        <span>🥔</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 工具入口
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="potato-card">
            <div class="potato-card-header">🔄 数据比对回填</div>
            <p style="color: #8B4513; font-size: 0.9rem;">将两个Excel文件按关键字段进行数据比对和回填</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("进入工具", key="go_compare", use_container_width=True):
            st.session_state.page = "数据比对回填"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="potato-card">
            <div class="potato-card-header">✂️ 数据拆分器</div>
            <p style="color: #8B4513; font-size: 0.9rem;">将大型Excel文件按指定条数拆分成多个文件</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("进入工具", key="go_split", use_container_width=True):
            st.session_state.page = "数据拆分器"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="potato-card">
            <div class="potato-card-header">🔗 数据聚合器</div>
            <p style="color: #8B4513; font-size: 0.9rem;">将相同数据的行合并，让内容聚合更高效</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("进入工具", key="go_aggregate", use_container_width=True):
            st.session_state.page = "数据聚合器"
            st.rerun()
    
    # 第二行工具
    col4, col5, col6, col7 = st.columns(4)
    
    with col4:
        st.markdown("""
        <div class="potato-card">
            <div class="potato-card-header">🌐 域名提取器</div>
            <p style="color: #8B4513; font-size: 0.9rem;">从URL中提取主域名或子域名</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("进入工具", key="go_domain", use_container_width=True):
            st.session_state.page = "域名提取器"
            st.rerun()
    
    with col5:
        st.markdown("""
        <div class="potato-card">
            <div class="potato-card-header">🌳 单位树构建器</div>
            <p style="color: #8B4513; font-size: 0.9rem;">根据单位数据自动构建组织架构树</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("进入工具", key="go_unit_tree", use_container_width=True):
            st.session_state.page = "单位树构建器"
            st.rerun()
    
    with col6:
        st.markdown("""
        <div class="potato-card">
            <div class="potato-card-header">🖥️ IP处理工具</div>
            <p style="color: #8B4513; font-size: 0.9rem;">IP段拆分与聚合，支持CIDR和范围格式</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("进入工具", key="go_ip_tool", use_container_width=True):
            st.session_state.page = "IP处理工具"
            st.rerun()
    
    with col7:
        st.markdown("""
        <div class="potato-card">
            <div class="potato-card-header">🚧 更多工具</div>
            <p style="color: #8B4513; font-size: 0.9rem;">更多实用工具正在开发中...</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💡 提交建议", use_container_width=True):
            st.info("💡 如有功能建议，欢迎联系开发者！")
    
    # 底部装饰
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #8B4513;">
        🥔 🍠 🥔 🍠 🥔
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
    
    # 文件上传区域
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 主表（文件1）")
        file1 = st.file_uploader(
            "点击选择Excel文件或将文件拖拽到此处",
            type=["xlsx", "xls", "csv"],
            key="file1"
        )
        
        if file1:
            with st.spinner("🥔 加载文件..."):
                df1 = load_data_file(file1)
                if df1 is not None:
                    st.session_state.df1 = df1
                    st.success(f"✅ 已加载：{file1.name}")
                    display_column_preview(df1)
    
    with col2:
        st.subheader("📁 数据源（文件2）")
        file2 = st.file_uploader(
            "点击选择Excel文件或将文件拖拽到此处",
            type=["xlsx", "xls", "csv"],
            key="file2"
        )
        
        if file2:
            with st.spinner("🍠 加载文件..."):
                df2 = load_data_file(file2)
                if df2 is not None:
                    st.session_state.df2 = df2
                    st.success(f"✅ 已加载：{file2.name}")
                    display_column_preview(df2)
    
    # 字段配置
    if st.session_state.df1 is not None and st.session_state.df2 is not None:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("⚙️ 字段配置")
        
        config_col1, config_col2, config_col3 = st.columns(3)
        
        with config_col1:
            match_col1 = st.selectbox(
                "🎯 主表匹配字段",
                options=st.session_state.df1.columns,
                help="选择主表中用于匹配的唯一标识字段"
            )
        
        with config_col2:
            match_col2 = st.selectbox(
                "🎯 数据源匹配字段",
                options=st.session_state.df2.columns,
                help="选择数据源中与主表匹配的字段"
            )
        
        with config_col3:
            fill_cols = st.multiselect(
                "🔄 回填字段",
                options=st.session_state.df2.columns,
                default=[],
                help="选择要从数据源回填到主表的字段"
            )
        
        # 执行比对
        if st.button("🚀 开始比对与回填", type="primary", use_container_width=True):
            with st.spinner("🥔 正在处理数据..."):
                try:
                    # 数据预处理
                    df1 = st.session_state.df1.copy()
                    df2 = st.session_state.df2.copy()
                    
                    # 统一匹配字段为字符串
                    df1[match_col1] = df1[match_col1].astype(str)
                    df2[match_col2] = df2[match_col2].astype(str)
                    
                    # 去重数据源
                    df2_unique = df2.drop_duplicates(subset=[match_col2], keep='first')
                    
                    # 重命名回填字段
                    df2_rename = df2_unique.rename(columns={col: f"{col}_来源" for col in fill_cols})
                    df2_rename = df2_rename.rename(columns={match_col2: match_col1})
                    
                    # 执行左连接
                    result_df = pd.merge(
                        df1,
                        df2_rename[[match_col1] + [f"{col}_来源" for col in fill_cols]],
                        on=match_col1,
                        how='left'
                    )
                    
                    # 统计信息
                    total_rows = len(df1)
                    matched_rows = result_df[result_df[f"{fill_cols[0]}_来源"].notna()].shape[0] if fill_cols else 0
                    match_rate = (matched_rows / total_rows * 100) if total_rows > 0 else 0
                    
                    st.session_state.result_df = result_df
                    st.session_state.stats = {
                        'total': total_rows,
                        'matched': matched_rows,
                        'match_rate': match_rate,
                        'fill_cols': fill_cols
                    }
                    
                    st.success("✅ 比对完成！")
                    
                except Exception as e:
                    st.error(f"❌ 处理失败：{str(e)}")
        
        # 显示结果
        if st.session_state.result_df is not None:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.subheader("📊 处理结果")
            
            # 统计卡片
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📝 总行数", f"{st.session_state.stats['total']:,}")
            with col2:
                st.metric("✅ 匹配成功", f"{st.session_state.stats['matched']:,}")
            with col3:
                st.metric("❌ 匹配失败", f"{st.session_state.stats['total'] - st.session_state.stats['matched']:,}")
            with col4:
                st.metric("✨ 回填单元格", f"{st.session_state.stats['matched'] * len(st.session_state.stats['fill_cols']):,}")
            
            # 结果预览
            with st.expander("👁️ 预览结果（前50行）", expanded=False):
                st.dataframe(st.session_state.result_df.head(50), use_container_width=True, height=300)
            
            # 下载按钮
            col_download1, col_download2 = st.columns(2)
            with col_download1:
                excel_bytes = excel_to_bytes(st.session_state.result_df)
                st.download_button(
                    label="📥 下载Excel结果",
                    data=excel_bytes,
                    file_name="数据比对结果.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            with col_download2:
                csv_bytes = csv_to_bytes(st.session_state.result_df)
                st.download_button(
                    label="📥 下载CSV结果",
                    data=csv_bytes,
                    file_name="数据比对结果.csv",
                    mime="text/csv",
                    use_container_width=True
                )


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
    
    # 文件上传
    st.subheader("📁 上传待拆分文件")
    file = st.file_uploader(
        "点击选择Excel/CSV文件或将文件拖拽到此处",
        type=["xlsx", "xls", "csv"],
        key="split_file"
    )
    
    if file:
        with st.spinner("🥔 加载文件..."):
            df = load_data_file(file)
            if df is not None:
                st.session_state.split_df = df
                st.success(f"✅ 已加载：{file.name} | {len(df):,} 行")
                display_column_preview(df)
                
                # 拆分设置
                st.markdown("<hr>", unsafe_allow_html=True)
                st.subheader("⚙️ 拆分设置")
                
                col1, col2 = st.columns(2)
                with col1:
                    split_size = st.number_input(
                        "🔢 每个文件行数",
                        min_value=100,
                        max_value=50000,
                        value=5000,
                        step=100
                    )
                with col2:
                    file_prefix = st.text_input("📛 文件前缀", value="拆分数据")
                
                # 计算拆分数量
                total_rows = len(df)
                split_count = (total_rows + split_size - 1) // split_size
                
                st.info(f"📊 拆分预估：{total_rows:,} 行 → {split_count} 个文件（每个{split_size:,}行）")
                
                # 执行拆分
                if st.button("🚀 开始拆分", type="primary", use_container_width=True):
                    with st.spinner("🥔 正在拆分文件..."):
                        try:
                            # 拆分数据
                            dfs = []
                            for i in range(split_count):
                                start = i * split_size
                                end = min((i + 1) * split_size, total_rows)
                                dfs.append(df.iloc[start:end])
                            
                            # 打包为ZIP
                            zip_data = excel_to_bytes_multi(dfs, file_prefix)
                            
                            st.session_state.split_result = {
                                'zip_data': zip_data,
                                'filename': f"{file_prefix}_拆分文件.zip",
                                'split_count': split_count
                            }
                            
                            st.success(f"✅ 拆分完成！生成{split_count}个文件")
                            
                        except Exception as e:
                            st.error(f"❌ 拆分失败：{str(e)}")
                
                # 下载按钮
                if st.session_state.split_result:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.subheader("📥 下载拆分文件")
                    
                    st.download_button(
                        label="📥 下载ZIP打包文件",
                        data=st.session_state.split_result['zip_data'],
                        file_name=st.session_state.split_result['filename'],
                        mime="application/zip",
                        use_container_width=True
                    )


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
    if 'aggregate_df' not in st.session_state:
        st.session_state.aggregate_df = None
    if 'aggregate_result' not in st.session_state:
        st.session_state.aggregate_result = None
    
    # 文件上传
    st.subheader("📁 上传待聚合文件")
    file = st.file_uploader(
        "点击选择Excel/CSV文件或将文件拖拽到此处",
        type=["xlsx", "xls", "csv"],
        key="aggregate_file"
    )
    
    if file:
        with st.spinner("🥔 加载文件..."):
            df = load_data_file(file)
            if df is not None:
                st.session_state.aggregate_df = df
                st.success(f"✅ 已加载：{file.name} | {len(df):,} 行")
                display_column_preview(df)
                
                # 聚合设置
                st.markdown("<hr>", unsafe_allow_html=True)
                st.subheader("⚙️ 聚合设置")
                
                group_cols = st.multiselect(
                    "🎯 分组字段（按这些字段分组聚合）",
                    options=df.columns,
                    default=[],
                    help="选择用于分组的字段（可多选）"
                )
                
                if group_cols:
                    # 选择聚合字段和方式
                    st.subheader("🔄 聚合字段配置")
                    agg_cols = st.multiselect(
                        "选择要聚合的字段",
                        options=[col for col in df.columns if col not in group_cols],
                        default=[]
                    )
                    
                    agg_methods = {}
                    for col in agg_cols:
                        method = st.selectbox(
                            f"{col} 聚合方式",
                            options=["拼接（逗号分隔）", "求和", "计数", "最大值", "最小值", "平均值"],
                            key=f"agg_{col}"
                        )
                        
                        method_map = {
                            "拼接（逗号分隔）": lambda x: ', '.join(x.dropna().unique()),
                            "求和": 'sum',
                            "计数": 'count',
                            "最大值": 'max',
                            "最小值": 'min',
                            "平均值": 'mean'
                        }
                        agg_methods[col] = method_map[method]
                    
                    # 执行聚合
                    if st.button("🚀 开始聚合", type="primary", use_container_width=True):
                        with st.spinner("🥔 正在聚合数据..."):
                            try:
                                # 执行分组聚合
                                result_df = df.groupby(group_cols).agg(agg_methods).reset_index()
                                
                                st.session_state.aggregate_result = result_df
                                st.success(f"✅ 聚合完成！从{len(df):,}行 → {len(result_df):,}行")
                                
                            except Exception as e:
                                st.error(f"❌ 聚合失败：{str(e)}")
                
                # 显示结果
                if st.session_state.aggregate_result is not None:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.subheader("📊 聚合结果")
                    
                    st.dataframe(st.session_state.aggregate_result.head(50), use_container_width=True, height=300)
                    
                    # 下载按钮
                    col_download1, col_download2 = st.columns(2)
                    with col_download1:
                        excel_bytes = excel_to_bytes(st.session_state.aggregate_result)
                        st.download_button(
                            label="📥 下载Excel结果",
                            data=excel_bytes,
                            file_name="数据聚合结果.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    with col_download2:
                        csv_bytes = csv_to_bytes(st.session_state.aggregate_result)
                        st.download_button(
                            label="📥 下载CSV结果",
                            data=csv_bytes,
                            file_name="数据聚合结果.csv",
                            mime="text/csv",
                            use_container_width=True
                        )


# ============================================
# 页面5：域名提取器
# ============================================
def show_domain_extractor():
    """显示域名提取器工具"""
    st.markdown("""
    <div class="potato-header">
        <h1 class="potato-title">🌐 域名提取器</h1>
        <p class="potato-subtitle">✨ 从URL中提取主域名或子域名 ✨</p>
    </div>
    
    <div class="potato-decoration">🥔 🍠 🥔 🍠 🥔</div>
    """, unsafe_allow_html=True)
    
    # 初始化session state
    if 'domain_df' not in st.session_state:
        st.session_state.domain_df = None
    if 'domain_result' not in st.session_state:
        st.session_state.domain_result = None
    
    # 文件上传
    st.subheader("📁 上传包含URL的文件")
    file = st.file_uploader(
        "点击选择Excel/CSV文件或将文件拖拽到此处",
        type=["xlsx", "xls", "csv"],
        key="domain_file"
    )
    
    if file:
        with st.spinner("🥔 加载文件..."):
            df = load_data_file(file)
            if df is not None:
                st.session_state.domain_df = df
                st.success(f"✅ 已加载：{file.name} | {len(df):,} 行")
                display_column_preview(df)
                
                # 字段配置
                st.markdown("<hr>", unsafe_allow_html=True)
                st.subheader("⚙️ 提取设置")
                
                col1, col2 = st.columns(2)
                with col1:
                    url_col = st.selectbox(
                        "🎯 URL字段",
                        options=df.columns,
                        help="选择包含URL的字段"
                    )
                with col2:
                    extract_type = st.selectbox(
                        "🔧 提取类型",
                        options=["主域名", "完整子域名"],
                        index=0,
                        help="选择提取主域名（如baidu.com）或完整子域名（如www.baidu.com）"
                    )
                
                # 执行提取
                if st.button("🚀 开始提取域名", type="primary", use_container_width=True):
                    with st.spinner("🥔 正在提取域名..."):
                        try:
                            # 提取域名
                            def extract_domain(url):
                                if pd.isna(url) or not str(url).strip():
                                    return ""
                                url = str(url).strip()
                                if not url.startswith(('http://', 'https://')):
                                    url = 'http://' + url
                                parsed = urlparse(url)
                                domain = parsed.netloc
                                if ':' in domain:
                                    domain = domain.split(':')[0]
                                
                                if extract_type == "主域名":
                                    parts = domain.split('.')
                                    if len(parts) >= 2:
                                        return '.'.join(parts[-2:])
                                    return domain
                                else:
                                    return domain
                            
                            df['提取域名'] = df[url_col].apply(extract_domain)
                            
                            st.session_state.domain_result = df
                            st.success("✅ 域名提取完成！")
                            
                        except Exception as e:
                            st.error(f"❌ 提取失败：{str(e)}")
                
                # 显示结果
                if st.session_state.domain_result is not None:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.subheader("📊 提取结果")
                    
                    st.dataframe(st.session_state.domain_result.head(50), use_container_width=True, height=300)
                    
                    # 下载按钮
                    col_download1, col_download2 = st.columns(2)
                    with col_download1:
                        excel_bytes = excel_to_bytes(st.session_state.domain_result)
                        st.download_button(
                            label="📥 下载Excel结果",
                            data=excel_bytes,
                            file_name="域名提取结果.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    with col_download2:
                        csv_bytes = csv_to_bytes(st.session_state.domain_result)
                        st.download_button(
                            label="📥 下载CSV结果",
                            data=csv_bytes,
                            file_name="域名提取结果.csv",
                            mime="text/csv",
                            use_container_width=True
                        )


# ============================================
# 页面6：单位树构建器
# ============================================
def show_unit_tree_tool():
    """显示单位树构建器工具"""
    st.markdown("""
    <div class="potato-header">
        <h1 class="potato-title">🌳 单位树构建器</h1>
        <p class="potato-subtitle">✨ 根据单位数据自动构建组织架构树 ✨</p>
    </div>
    
    <div class="potato-decoration">🥔 🍠 🥔 🍠 🥔</div>
    """, unsafe_allow_html=True)
    
    # 初始化session state
    if 'unit_tree_df' not in st.session_state:
        st.session_state.unit_tree_df = None
    if 'unit_tree_result' not in st.session_state:
        st.session_state.unit_tree_result = None
    
    # 文件上传
    st.subheader("📁 上传单位数据文件")
    file = st.file_uploader(
        "点击选择Excel/CSV文件或将文件拖拽到此处",
        type=["xlsx", "xls", "csv"],
        key="unit_tree_file"
    )
    
    if file:
        with st.spinner("🥔 加载文件..."):
            df = load_data_file(file)
            if df is not None:
                st.session_state.unit_tree_df = df
                st.success(f"✅ 已加载：{file.name} | {len(df):,} 行")
                display_column_preview(df)
                
                # 字段配置
                st.markdown("<hr>", unsafe_allow_html=True)
                st.subheader("⚙️ 字段配置")
                
                col1, col2 = st.columns(2)
                with col1:
                    unit_col = st.selectbox(
                        "🎯 单位名称字段",
                        options=df.columns,
                        help="选择包含单位名称的字段"
                    )
                with col2:
                    region_col = st.selectbox(
                        "🌍 区域字段（可选）",
                        options=["无"] + list(df.columns),
                        help="选择按区域分组的字段"
                    )
                
                # 执行构建
                if st.button("🚀 开始构建单位树", type="primary", use_container_width=True):
                    with st.spinner("🥔 正在构建单位树..."):
                        try:
                            # 简单的单位树构建逻辑
                            unit_list = df[unit_col].dropna().unique().tolist()
                            
                            # 构建层级
                            tree_data = []
                            for unit in unit_list:
                                # 简单层级判定
                                if '省' in unit or '市' in unit:
                                    level = '省级/市级'
                                elif '区' in unit or '县' in unit:
                                    level = '区级/县级'
                                elif '街道' in unit or '镇' in unit:
                                    level = '街道/镇级'
                                else:
                                    level = '其他'
                                
                                tree_data.append({
                                    '单位名称': unit,
                                    '层级': level,
                                    '上级单位': None
                                })
                            
                            result_df = pd.DataFrame(tree_data)
                            st.session_state.unit_tree_result = result_df
                            
                            st.success("✅ 单位树构建完成！")
                            
                        except Exception as e:
                            st.error(f"❌ 构建失败：{str(e)}")
                
                # 显示结果
                if st.session_state.unit_tree_result is not None:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.subheader("📊 单位树结果")
                    
                    st.dataframe(st.session_state.unit_tree_result, use_container_width=True, height=300)
                    
                    # 下载按钮
                    col_download1, col_download2 = st.columns(2)
                    with col_download1:
                        excel_bytes = excel_to_bytes(st.session_state.unit_tree_result)
                        st.download_button(
                            label="📥 下载Excel结果",
                            data=excel_bytes,
                            file_name="单位树结果.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    with col_download2:
                        csv_bytes = csv_to_bytes(st.session_state.unit_tree_result)
                        st.download_button(
                            label="📥 下载CSV结果",
                            data=csv_bytes,
                            file_name="单位树结果.csv",
                            mime="text/csv",
                            use_container_width=True
                        )


# ============================================
# 页面7：IP处理工具
# ============================================
def show_ip_tool():
    """显示IP处理工具"""
    st.markdown("""
    <div class="potato-header">
        <h1 class="potato-title">🖥️ IP处理工具</h1>
        <p class="potato-subtitle">✨ IP段拆分与聚合，支持CIDR和范围格式 ✨</p>
    </div>
    
    <div class="potato-decoration">🥔 🍠 🥔 🍠 🥔</div>
    """, unsafe_allow_html=True)
    
    # 初始化session state
    if 'ip_df' not in st.session_state:
        st.session_state.ip_df = None
    if 'ip_result' not in st.session_state:
        st.session_state.ip_result = None
    
    # 文件上传
    st.subheader("📁 上传IP数据文件")
    file = st.file_uploader(
        "点击选择Excel/CSV文件或将文件拖拽到此处",
        type=["xlsx", "xls", "csv"],
        key="ip_file"
    )
    
    if file:
        with st.spinner("🥔 加载文件..."):
            df = load_data_file(file)
            if df is not None:
                st.session_state.ip_df = df
                st.success(f"✅ 已加载：{file.name} | {len(df):,} 行")
                display_column_preview(df)
                
                # 字段配置
                st.markdown("<hr>", unsafe_allow_html=True)
                st.subheader("⚙️ 处理设置")
                
                col1, col2 = st.columns(2)
                with col1:
                    ip_col = st.selectbox(
                        "🎯 IP字段",
                        options=df.columns,
                        help="选择包含IP/IP段的字段"
                    )
                with col2:
                    process_mode = st.selectbox(
                        "🔧 处理模式",
                        options=["IP拆分（段→单个IP）", "IP聚合（单个IP→段）"],
                        index=0,
                        help="选择处理模式"
                    )
                
                # 执行处理
                if st.button("🚀 开始处理IP", type="primary", use_container_width=True):
                    with st.spinner("🥔 正在处理IP..."):
                        try:
                            # IP处理函数
                            def parse_ip_range(ip_str):
                                if pd.isna(ip_str) or not str(ip_str).strip():
                                    return [], "空值"
                                ip_str = str(ip_str).strip()
                                
                                try:
                                    if '/' in ip_str:
                                        network = ipaddress.ip_network(ip_str, strict=False)
                                        return [str(ip) for ip in network.hosts()], None
                                    elif '-' in ip_str:
                                        parts = ip_str.split('-')
                                        if len(parts) != 2:
                                            return [], "格式错误"
                                        start = int(ipaddress.IPv4Address(parts[0].strip()))
                                        end = int(ipaddress.IPv4Address(parts[1].strip()))
                                        return [str(ipaddress.IPv4Address(ip)) for ip in range(start, end+1)], None
                                    else:
                                        ipaddress.IPv4Address(ip_str)
                                        return [ip_str], None
                                except Exception as e:
                                    return [], f"错误: {str(e)}"
                            
                            # 处理数据
                            result_data = []
                            for idx, row in df.iterrows():
                                ip_str = row[ip_col]
                                ips, error = parse_ip_range(ip_str)
                                
                                if process_mode == "IP拆分（段→单个IP）":
                                    if error:
                                        result_data.append({
                                            '原始IP段': ip_str,
                                            '处理后IP': '',
                                            '错误信息': error
                                        })
                                    else:
                                        for ip in ips:
                                            result_data.append({
                                                '原始IP段': ip_str,
                                                '处理后IP': ip,
                                                '错误信息': ''
                                            })
                                else:
                                    # 聚合模式
                                    if ips:
                                        aggregated = ', '.join(ips)
                                        result_data.append({
                                            '原始IP': ip_str,
                                            '聚合后IP段': aggregated,
                                            '错误信息': ''
                                        })
                                    else:
                                        result_data.append({
                                            '原始IP': ip_str,
                                            '聚合后IP段': '',
                                            '错误信息': error
                                        })
                            
                            result_df = pd.DataFrame(result_data)
                            st.session_state.ip_result = result_df
                            
                            st.success("✅ IP处理完成！")
                            
                        except Exception as e:
                            st.error(f"❌ 处理失败：{str(e)}")
                
                # 显示结果
                if st.session_state.ip_result is not None:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.subheader("📊 IP处理结果")
                    
                    st.dataframe(st.session_state.ip_result.head(50), use_container_width=True, height=300)
                    
                    # 下载按钮
                    col_download1, col_download2 = st.columns(2)
                    with col_download1:
                        excel_bytes = excel_to_bytes(st.session_state.ip_result)
                        st.download_button(
                            label="📥 下载Excel结果",
                            data=excel_bytes,
                            file_name="IP处理结果.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    with col_download2:
                        csv_bytes = csv_to_bytes(st.session_state.ip_result)
                        st.download_button(
                            label="📥 下载CSV结果",
                            data=csv_bytes,
                            file_name="IP处理结果.csv",
                            mime="text/csv",
                            use_container_width=True
                        )


# ============================================
# 主程序入口
# ============================================
def main():
    """主函数"""
    # 初始化session state
    if 'page' not in st.session_state:
        st.session_state.page = "首页"
    
    # 侧边栏导航
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <span style="font-size: 3rem;">🥔</span>
            <h2 style="color: #8B4513; margin: 0.5rem 0;">土豆数据小助手</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # 导航菜单
        nav_pages = [
            "首页",
            "数据比对回填",
            "数据拆分器",
            "数据聚合器",
            "域名提取器",
            "单位树构建器",
            "IP处理工具"
        ]
        
        selected_page = st.selectbox(
            "🔍 选择工具",
            options=nav_pages,
            index=nav_pages.index(st.session_state.page)
        )
        
        if selected_page != st.session_state.page:
            st.session_state.page = selected_page
            st.rerun()
        
        st.divider()
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <span style="font-size: 2rem;">🥔 🍠 🥔</span>
        </div>
        """, unsafe_allow_html=True)
        st.caption("🥔 v2.5 工具箱版")
    
    # 页面路由
    if st.session_state.page == "首页":
        show_home()
    elif st.session_state.page == "数据比对回填":
        show_compare_tool()
    elif st.session_state.page == "数据拆分器":
        show_split_tool()
    elif st.session_state.page == "数据聚合器":
        show_aggregate_tool()
    elif st.session_state.page == "域名提取器":
        show_domain_extractor()
    elif st.session_state.page == "单位树构建器":
        show_unit_tree_tool()
    elif st.session_state.page == "IP处理工具":
        show_ip_tool()


if __name__ == "__main__":
    main()
