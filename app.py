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


def load_data_file(file) -> pd.DataFrame:
    """统一加载Excel和CSV文件"""
    file_name = file.name.lower()
    
    if file_name.endswith(('.xlsx', '.xls')):
        try:
            return pd.read_excel(file, engine='openpyxl' if file_name.endswith('.xlsx') else 'xlrd')
        except Exception as e:
            st.error(f"❌ Excel文件加载失败: {str(e)}")
            return None
    elif file_name.endswith('.csv'):
        return load_csv_file(file)
    else:
        st.error(f"❌ 不支持的文件格式: {file_name}")
        return None


def csv_to_bytes(df: pd.DataFrame, filename: str = "result.csv") -> bytes:
    """将DataFrame转换为CSV字节流用于下载"""
    output = StringIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    output.seek(0)
    return output.getvalue()


def excel_to_bytes(df: pd.DataFrame, filename: str = "result.xlsx") -> bytes:
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
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">❓ 空值数量</div>
            <div class="metric-value">{df.isnull().sum().sum()}</div>
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
# IP处理工具函数
# ============================================
def parse_ip_range(ip_str: str) -> tuple[list, str]:
    """解析IP段，返回 (IP列表, 错误信息)
    
    支持格式：
    - 单个IP：192.168.1.1
    - 范围格式：192.168.1.1-192.168.1.10
    - CIDR格式：192.168.1.0/24
    
    Args:
        ip_str: IP字符串
    
    Returns:
        (IP列表, 错误信息) - 成功时错误信息为None
    """
    if pd.isna(ip_str) or not str(ip_str).strip():
        return [], "空值"
    
    ip_str = str(ip_str).strip()
    
    if not ip_str:
        return [], "空值"
    
    try:
        # CIDR格式
        if '/' in ip_str:
            network = ipaddress.ip_network(ip_str, strict=False)
            return [str(ip) for ip in network.hosts()], None
        
        # 范围格式
        if '-' in ip_str:
            parts = ip_str.split('-')
            if len(parts) != 2:
                return [], "范围格式错误（应使用-连接）"
            
            start_ip = parts[0].strip()
            end_ip = parts[1].strip()
            
            start = int(ipaddress.IPv4Address(start_ip))
            end = int(ipaddress.IPv4Address(end_ip))
            
            if start > end:
                return [], "起始IP大于结束IP"
            
            return [str(ipaddress.IPv4Address(ip)) for ip in range(start, end + 1)], None
        
        # 单个IP
        ipaddress.IPv4Address(ip_str)
        return [ip_str], None
    
    except ipaddress.AddressValueError as e:
        return [], f"IP格式无效: {str(e)}"
    except ValueError as e:
        return [], f"解析错误: {str(e)}"
    except Exception as e:
        return [], f"未知错误: {str(e)}"


def aggregate_ips_continuous(ip_list: list) -> list:
    """聚合连续IP为IP段（连续模式）
    
    将连续的IP聚合成IP段，非连续的保留
    
    Args:
        ip_list: IP列表
    
    Returns:
        聚合后的IP列表（连续的成段，不连续的保留单个IP）
    """
    if not ip_list:
        return []
    
    # 转换为整数并排序
    ip_ints = sorted([int(ipaddress.IPv4Address(ip)) for ip in ip_list])
    
    ranges = []
    start = ip_ints[0]
    end = ip_ints[0]
    
    for ip in ip_ints[1:]:
        if ip == end + 1:
            end = ip
        else:
            if start == end:
                ranges.append(str(ipaddress.IPv4Address(start)))
            else:
                ranges.append(f"{ipaddress.IPv4Address(start)}-{ipaddress.IPv4Address(end)}")
            start = ip
            end = ip
    
    # 添加最后一个范围
    if start == end:
        ranges.append(str(ipaddress.IPv4Address(start)))
    else:
        ranges.append(f"{ipaddress.IPv4Address(start)}-{ipaddress.IPv4Address(end)}")
    
    return ranges


def aggregate_ips_mixed(ip_list: list) -> str:
    """聚合IP（混合模式：连续的成段，不连续的保留）
    
    Args:
        ip_list: IP列表
    
    Returns:
        用逗号分隔的聚合结果
    """
    ranges = aggregate_ips_continuous(ip_list)
    return ', '.join(ranges)

# ============================================
# 域名提取工具函数
# ============================================
def extract_domain(url: str, extract_main_domain: bool = True) -> str:
    """从URL中提取域名
    
    Args:
        url: 网址字符串
        extract_main_domain: 是否提取主域名（True）或子域名（False）
    
    Returns:
        提取的域名，失败返回空字符串
    """
    if pd.isna(url) or not str(url).strip():
        return ""
    
    url = str(url).strip()
    
    # 处理没有http/https的URL
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        
        # 移除端口号
        if ':' in domain:
            domain = domain.split(':')[0]
        
        # 处理政务域名特殊情况
        if extract_main_domain:
            # 提取主域名（保留二级域名）
            parts = domain.split('.')
            if len(parts) >= 2:
                # 政务域名处理
                if len(parts) >= 3 and parts[-2] in ['gov', 'cn', 'com']:
                    if parts[-3] in ['gov', 'cn']:
                        return '.'.join(parts[-3:])
                return '.'.join(parts[-2:])
            return domain
        else:
            # 返回完整子域名
            return domain
    except Exception as e:
        # 备用正则提取
        match = re.search(r'(?:https?://)?([^/:]+)', url)
        if match:
            return match.group(1)
        return ""

# ============================================
# 单位树构建工具函数
# ============================================
def build_unit_tree(df, unit_col, code_col=None, region_col=None):
    """构建单位树结构"""
    unit_tree = {}
    
    # 清理单位名称
    def clean_unit_name(name):
        if pd.isna(name):
            return ""
        name = str(name).strip()
        # 移除常见后缀
        suffixes = ['有限公司', '有限责任公司', '股份有限公司', '分公司', '办事处', '营业部', '支行']
        for suffix in suffixes:
            if name.endswith(suffix):
                name = name[:-len(suffix)]
        return name
    
    df['clean_unit_name'] = df[unit_col].apply(clean_unit_name)
    
    # 按区域分组（如果有区域字段）
    if region_col and region_col in df.columns:
        regions = df[region_col].dropna().unique()
        for region in regions:
            region_df = df[df[region_col] == region]
            unit_tree[region] = {}
            
            # 提取单位关键词
            for idx, row in region_df.iterrows():
                unit_name = row['clean_unit_name']
                unit_code = row[code_col] if code_col else idx
                
                # 简单的层级判定
                if '省' in unit_name or '市' in unit_name:
                    level = '省级'
                elif '区' in unit_name or '县' in unit_name:
                    level = '市级/区级'
                elif '街道' in unit_name or '镇' in unit_name:
                    level = '街道/镇级'
                else:
                    level = '其他'
                
                unit_tree[region][unit_code] = {
                    'name': row[unit_col],
                    'clean_name': unit_name,
                    'level': level,
                    'parent': None,
                    'children': []
                }
    else:
        # 无区域分组
        for idx, row in df.iterrows():
            unit_name = row['clean_unit_name']
            unit_code = row[code_col] if code_col else idx
            
            if '省' in unit_name or '市' in unit_name:
                level = '省级'
            elif '区' in unit_name or '县' in unit_name:
                level = '市级/区级'
            elif '街道' in unit_name or '镇' in unit_name:
                level = '街道/镇级'
            else:
                level = '其他'
            
            unit_tree[unit_code] = {
                'name': row[unit_col],
                'clean_name': unit_name,
                'level': level,
                'parent': None,
                'children': []
            }
    
    return unit_tree

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
    
    # 工具2：数据聚合器 + 域名提取器
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
        <div class="tool-card" style="padding-bottom: 0.5rem;">
            <div class="tool-icon">🌐</div>
            <div class="tool-title">域名提取器</div>
            <div class="tool-desc">从URL中提取主域名或子域名</div>
            <p style="margin-top: 0.5rem; color: #8B4513; font-size: 0.85rem;">
                📁 上传Excel文件 → 选择URL字段 → 自动提取域名
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 进入工具", key="go_domain", use_container_width=True):
            st.session_state.page = "🌐 域名提取器"
            st.rerun()
    
    # 工具3：单位树构建器 + IP处理工具
    st.markdown("---")
    col5, col6 = st.columns(2, gap="large")
    
    with col5:
        st.markdown("""
        <div class="tool-card" style="padding-bottom: 0.5rem;">
            <div class="tool-icon">🌳</div>
            <div class="tool-title">单位树构建器</div>
            <div class="tool-desc">根据单位数据自动构建组织架构树</div>
            <p style="margin-top: 0.5rem; color: #8B4513; font-size: 0.85rem;">
                📁 上传数据 → 字段映射 → 自动分组与上级判定
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 进入工具", key="go_unit_tree", use_container_width=True):
            st.session_state.page = "🌳 单位树构建器"
            st.rerun()
    
    with col6:
        st.markdown("""
        <div class="tool-card" style="padding-bottom: 0.5rem;">
            <div class="tool-icon">🖥️</div>
            <div class="tool-title">IP处理工具</div>
            <div class="tool-desc">IP段拆分与聚合，支持CIDR和范围格式</div>
            <p style="margin-top: 0.5rem; color: #8B4513; font-size: 0.85rem;">
                📁 上传数据 → 选择模式 → IP拆分/聚合
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 进入工具", key="go_ip_tool", use_container_width=True):
            st.session_state.page = "🖥️ IP处理工具"
            st.rerun()
    
    # 更多工具占位
    col7 = st.columns(1)[0]
    with col7:
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
        if st.button("💡 提交功能建议", key="go_more_tools", use_container_width=True):
            st.info("💡 如有功能建议或需求，欢迎联系开发者！")
    
    # 版本更新
    st.markdown("""
    <div class="potato-card" style="margin: 1.5rem 0;">
        <div class="potato-card-header">📝 版本更新</div>
        
        <div style="margin-top: 1rem; color: #8B4513;">
            <p style="margin: 0.5rem 0; font-weight: 600;">
                <span style="background: linear-gradient(135deg, #FF6B6B, #FF4757); color: white; padding: 0.15rem 0.6rem; border-radius: 15px; font-size: 0.8rem; margin-right: 0.5rem;">🖥️ v2.4</span>
                当前版本
            </p>
            <ul style="margin: 0.3rem 0; padding-left: 2rem; line-height: 1.8; font-size: 0.9rem;">
                <li>新增IP处理工具功能</li>
                <li>支持IP段拆分（CIDR和范围格式）</li>
                <li>支持IP聚合（连续和混合模式）</li>
                <li>同一单位数据隔离处理</li>
            </ul>
            
            <p style="margin: 1rem 0 0.5rem 0; font-weight: 600;">
                <span style="background: linear-gradient(135deg, #32CD32, #228B22); color: white; padding: 0.15rem 0.6rem; border-radius: 15px; font-size: 0.8rem; margin-right: 0.5rem;">🌳 v2.3</span>
            </p>
            <ul style="margin: 0.3rem 0; padding-left: 2rem; line-height: 1.8; font-size: 0.9rem;">
                <li>新增单位树构建器功能</li>
                <li>支持10种分组自动判定</li>
                <li>智能上级节点判定</li>
                <li>支持按分组和区域筛选预览</li>
            </ul>
            
            <p style="margin: 1rem 0 0.5rem 0; font-weight: 600;">
                <span style="background: linear-gradient(135deg, #FFA500, #FF8C00); color: white; padding: 0.15rem 0.6rem; border-radius: 15px; font-size: 0.8rem; margin-right: 0.5rem;">🥔 v2.2</span>
                域名提取器版
            </p>
            <ul style="margin: 0.3rem 0; padding-left: 2rem; line-height: 1.8; font-size: 0.9rem;">
                <li>新增域名提取器功能</li>
                <li>支持政务类域名和普通域名</li>
                <li>支持提取主域名和子域名</li>
            </ul>
            
            <p style="margin: 1rem 0 0.5rem 0; font-weight: 600;">
                <span style="background: #D2691E; color: white; padding: 0.15rem 0.6rem; border-radius: 15px; font-size: 0.8rem; margin-right: 0.5rem;">🍠 v2.0</span>
                工具箱版
            </p>
            <ul style="margin: 0.3rem 0; padding-left: 2rem; line-height: 1.8; font-size: 0.9rem;">
                <li>重构为多工具集架构</li>
                <li>新增数据拆分器功能</li>
                <li>土豆主题UI优化</li>
            </ul>
            
            <p style="margin: 1rem 0 0.5rem 0; font-weight: 600;">
                <span style="background: #8B4513; color: white; padding: 0.15rem 0.6rem; border-radius: 15px; font-size: 0.8rem; margin-right: 0.5rem;">🥔 v1.0</span>
                初始版本
            </p>
            <ul style="margin: 0.3rem 0; padding-left: 2rem; line-height: 1.8; font-size: 0.9rem;">
                <li>数据比对回填功能</li>
                <li>可爱土豆风格界面</li>
            </ul>
        </div>
    </div>
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
    
    # 使用说明卡片
    st.markdown("""
    <div class="potato-card" style="margin: 1rem 0;">
        <div style="display: flex; flex-wrap: wrap; gap: 1rem;">
            <div style="flex: 1; min-width: 250px;">
                <div style="color: #8B4513; font-weight: 600; margin-bottom: 0.5rem;">📖 工具用途</div>
                <div style="color: #D2691E; font-size: 0.9rem;">将两个Excel文件按关键字段进行数据比对和回填，适合数据整合场景。</div>
            </div>
            <div style="flex: 2; min-width: 300px;">
                <div style="color: #8B4513; font-weight: 600; margin-bottom: 0.5rem;">📋 使用步骤</div>
                <div style="color: #8B4513; font-size: 0.9rem;">
                    ① 上传主表 → ② 上传数据源 → ③ 选择匹配字段 → ④ 选择回填字段 → ⑤ 执行回填
                </div>
            </div>
        </div>
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
                <li>上传 <b>主表</b> 📁（支持 Excel/CSV）</li>
                <li>上传 <b>数据源</b> 📁（支持 Excel/CSV）</li>
                <li>选择 <b>匹配字段</b> 🔍</li>
                <li>选择 <b>回填字段</b> 🔄</li>
                <li>点击 <b>开始比对</b> 🚀</li>
                <li>下载 <b>结果文件</b> 📥（Excel/CSV）</li>
            </ol>
        </div>
        
        <div class="potato-card">
            <div class="potato-card-header">💡 温馨提示</div>
            <ul style="color: #8B4513; line-height: 1.7; font-size: 0.9rem; padding-left: 1.2rem;">
                <li>支持 .xlsx .xls .csv 格式</li>
                <li>CSV自动检测编码（UTF-8/GBK）</li>
                <li>大文件使用批量merge加速</li>
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
            type=['xlsx', 'xls', 'csv'],
            help="🥔 主表将作为输出文件的基础（支持 .xlsx .xls .csv）",
            key="file_uploader_1"
        )
        
        if file1:
            with st.spinner("🥔 加载中..."):
                df1 = load_data_file(file1)
                if df1 is not None:
                    st.session_state.df1 = df1
                    # 显示文件信息
                    file_size_mb = file1.size / (1024 * 1024)
                    st.markdown(f"""
                    <div style="background: #E8F5E9; padding: 0.5rem 1rem; border-radius: 8px; margin: 0.5rem 0;">
                        <span style="color: #2E7D32; font-size: 0.85rem;">
                            📄 {file1.name} ({file_size_mb:.2f} MB) | 📝 {len(df1):,} 行 × {len(df1.columns)} 列
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("""
                    <div class="success-cute">✅ 已加载主表文件</div>
                    """, unsafe_allow_html=True)
                    display_column_preview(df1)
    
    with col2:
        st.markdown('<div class="potato-card"><div class="potato-card-header">📁 数据源（文件2）</div></div>', unsafe_allow_html=True)
        
        file2 = st.file_uploader(
            "点击上传或拖拽文件到此处",
            type=['xlsx', 'xls', 'csv'],
            help="🍠 数据源提供要回填的数据（支持 .xlsx .xls .csv）",
            key="file_uploader_2"
        )
        
        if file2:
            with st.spinner("🍠 加载中..."):
                df2 = load_data_file(file2)
                if df2 is not None:
                    st.session_state.df2 = df2
                    # 显示文件信息
                    file_size_mb = file2.size / (1024 * 1024)
                    st.markdown(f"""
                    <div style="background: #E8F5E9; padding: 0.5rem 1rem; border-radius: 8px; margin: 0.5rem 0;">
                        <span style="color: #2E7D32; font-size: 0.85rem;">
                            📄 {file2.name} ({file_size_mb:.2f} MB) | 📝 {len(df2):,} 行 × {len(df2.columns)} 列
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
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
        
        # 大文件警告
        total_rows = len(st.session_state.df1) + len(st.session_state.df2)
        is_large_file = total_rows > 100000
        
        if is_large_file:
            st.markdown(f"""
            <div style="background: #FFF3E0; padding: 1rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid #FF9800;">
                <div style="color: #E65100; font-weight: 600; margin-bottom: 0.3rem;">
                    ⚠️ 大文件检测到
                </div>
                <div style="color: #8B4513; font-size: 0.9rem;">
                    检测到文件总行数超过10万行（{total_rows:,}行），比对可能需要较长时间，请耐心等待...
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 执行比对
        col_execute, col_clear = st.columns([1, 4])
        
        with col_execute:
            execute_btn = st.button(
                "🚀 开始比对回填",
                use_container_width=True,
                disabled=not (match_col1 and match_col2 and fill_cols)
            )
        
        with col_clear:
            if st.button("🧹 清空数据", use_container_width=True):
                st.session_state.df1 = None
                st.session_state.df2 = None
                st.session_state.result_df = None
                st.session_state.stats = None
                st.rerun()
        
        if execute_btn:
            with st.spinner("🥔 正在比对数据，请稍候..."):
                try:
                    # 创建数据副本
                    df1_copy = st.session_state.df1.copy()
                    df2_copy = st.session_state.df2.copy()
                    
                    # 清理匹配字段的空值
                    df1_copy = df1_copy.dropna(subset=[match_col1])
                    df2_copy = df2_copy.dropna(subset=[match_col2])
                    
                    # 确保匹配字段类型一致
                    df1_copy[match_col1] = df1_copy[match_col1].astype(str)
                    df2_copy[match_col2] = df2_copy[match_col2].astype(str)
                    
                    # 只保留需要的字段
                    df2_needed = df2_copy[[match_col2] + fill_cols].drop_duplicates(subset=[match_col2])
                    
                    # 重命名回填字段
                    rename_dict = {col: f"{col}_来源" for col in fill_cols}
                    df2_needed = df2_needed.rename(columns=rename_dict)
                    df2_needed = df2_needed.rename(columns={match_col2: match_col1})
                    
                    # 执行合并
                    result_df = pd.merge(
                        df1_copy,
                        df2_needed,
                        on=match_col1,
                        how='left'
                    )
                    
                    # 统计信息
                    total_rows = len(df1_copy)
                    matched_rows = result_df[result_df[f"{fill_cols[0]}_来源"].notna()].shape[0] if fill_cols else 0
                    match_rate = (matched_rows / total_rows * 100) if total_rows > 0 else 0
                    
                    st.session_state.result_df = result_df
                    st.session_state.stats = {
                        'total': total_rows,
                        'matched': matched_rows,
                        'match_rate': match_rate,
                        'fields_added': len(fill_cols)
                    }
                    
                    st.markdown("""
                    <div class="success-cute">
                        ✅ 数据比对回填完成！
                    </div>
                    """, unsafe_allow_html=True)
                
                except Exception as e:
                    st.markdown(f"""
                    <div class="error-cute">
                        ❌ 处理失败：{str(e)}
                    </div>
                    """, unsafe_allow_html=True)
        
        # 显示结果
        if st.session_state.result_df is not None and st.session_state.stats is not None:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<div class="potato-card"><div class="potato-card-header">📊 处理结果</div></div>', unsafe_allow_html=True)
            
            # 显示统计信息
            stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
            
            with stats_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📝 总行数</div>
                    <div class="metric-value">{st.session_state.stats['total']:,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with stats_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">✅ 匹配行数</div>
                    <div class="metric-value">{st.session_state.stats['matched']:,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with stats_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📈 匹配率</div>
                    <div class="metric-value">{st.session_state.stats['match_rate']:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with stats_col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">➕ 新增字段</div>
                    <div class="metric-value">{st.session_state.stats['fields_added']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # 结果预览
            st.markdown("### 📋 结果预览")
            st.dataframe(st.session_state.result_df.head(20), use_container_width=True, height=280)
            
            # 下载按钮
            st.markdown("<hr>", unsafe_allow_html=True)
            col_download_excel, col_download_csv = st.columns(2)
            
            with col_download_excel:
                excel_data = excel_to_bytes(st.session_state.result_df, "数据比对结果.xlsx")
                st.download_button(
                    label="📥 下载Excel格式",
                    data=excel_data,
                    file_name="数据比对结果.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col_download_csv:
                csv_data = csv_to_bytes(st.session_state.result_df, "数据比对结果.csv")
                st.download_button(
                    label="📥 下载CSV格式",
                    data=csv_data,
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
    
    # 使用说明
    st.markdown("""
    <div class="potato-card" style="margin: 1rem 0;">
        <div style="display: flex; flex-wrap: wrap; gap: 1rem;">
            <div style="flex: 1; min-width: 250px;">
                <div style="color: #8B4513; font-weight: 600; margin-bottom: 0.5rem;">📖 工具用途</div>
                <div style="color: #D2691E; font-size: 0.9rem;">将大型Excel/CSV文件按指定行数拆分成多个小文件，便于处理和分发。</div>
            </div>
            <div style="flex: 2; min-width: 300px;">
                <div style="color: #8B4513; font-weight: 600; margin-bottom: 0.5rem;">📋 使用步骤</div>
                <div style="color: #8B4513; font-size: 0.9rem;">
                    ① 上传文件 → ② 设置拆分条数 → ③ 执行拆分 → ④ 下载打包文件
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 侧边栏说明
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
                <li>上传 <b>待拆分文件</b> 📁（Excel/CSV）</li>
                <li>设置 <b>拆分条数</b> 🔢（每个文件的行数）</li>
                <li>点击 <b>开始拆分</b> 🚀</li>
                <li>下载 <b>ZIP打包文件</b> 📥</li>
            </ol>
        </div>
        
        <div class="potato-card">
            <div class="potato-card-header">💡 温馨提示</div>
            <ul style="color: #8B4513; line-height: 1.7; font-size: 0.9rem; padding-left: 1.2rem;">
                <li>支持 .xlsx .xls .csv 格式</li>
                <li>默认按5000行拆分，可自定义</li>
                <li>拆分后自动打包为ZIP文件</li>
                <li>保留原始文件的所有字段</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem;">
            <span style="font-size: 2rem;">✂️ 🥔</span>
        </div>
        """, unsafe_allow_html=True)
        st.caption("🥔 数据拆分器")
    
    # 初始化session state
    if 'split_df' not in st.session_state:
        st.session_state.split_df = None
    if 'split_result' not in st.session_state:
        st.session_state.split_result = None
    
    # 文件上传
    st.markdown('<div class="potato-card"><div class="potato-card-header">📁 上传待拆分文件</div></div>', unsafe_allow_html=True)
    
    file = st.file_uploader(
        "点击上传或拖拽文件到此处",
        type=['xlsx', 'xls', 'csv'],
        help="🥔 支持Excel和CSV格式文件",
        key="split_file_uploader"
    )
    
    if file:
        with st.spinner("🥔 加载文件中..."):
            df = load_data_file(file)
            if df is not None:
                st.session_state.split_df = df
                
                # 显示文件信息
                file_size_mb = file.size / (1024 * 1024)
                st.markdown(f"""
                <div style="background: #E8F5E9; padding: 0.5rem 1rem; border-radius: 8px; margin: 0.5rem 0;">
                    <span style="color: #2E7D32; font-size: 0.85rem;">
                        📄 {file.name} ({file_size_mb:.2f} MB) | 📝 {len(df):,} 行 × {len(df.columns)} 列
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
                # 显示数据预览
                st.markdown("### 📋 数据预览")
                st.dataframe(df.head(10), use_container_width=True, height=200)
                
                # 拆分设置
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown('<div class="potato-card"><div class="potato-card-header">⚙️ 拆分设置</div></div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    split_size = st.number_input(
                        "🔢 每个文件行数",
                        min_value=100,
                        max_value=50000,
                        value=5000,
                        step=100,
                        help="设置每个拆分文件包含的行数"
                    )
                
                with col2:
                    file_prefix = st.text_input(
                        "📛 文件前缀",
                        value="拆分数据",
                        help="拆分后的文件名称前缀"
                    )
                
                with col3:
                    file_format = st.selectbox(
                        "📄 输出格式",
                        options=["Excel (.xlsx)", "CSV (.csv)"],
                        index=0,
                        help="选择拆分文件的输出格式"
                    )
                
                # 计算拆分数量
                total_rows = len(df)
                split_count = (total_rows + split_size - 1) // split_size
                
                st.markdown(f"""
                <div style="background: #FFF8DC; padding: 1rem; border-radius: 12px; margin: 1rem 0;">
                    <div style="color: #8B4513; font-weight: 600;">📊 拆分预估</div>
                    <div style="color: #D2691E; margin-top: 0.5rem;">
                        • 总行数：<b>{total_rows:,}</b> 行<br>
                        • 拆分条数：<b>{split_size:,}</b> 行/文件<br>
                        • 生成文件数：<b>{split_count}</b> 个文件
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 执行拆分
                col_execute, col_clear = st.columns([1, 4])
                
                with col_execute:
                    if st.button("🚀 开始拆分", use_container_width=True):
                        with st.spinner("🥔 正在拆分文件，请稍候..."):
                            try:
                                # 拆分数据
                                dfs = []
                                for i in range(split_count):
                                    start_idx = i * split_size
                                    end_idx = min((i + 1) * split_size, total_rows)
                                    split_df = df.iloc[start_idx:end_idx]
                                    dfs.append(split_df)
                                
                                # 生成下载文件
                                if file_format == "Excel (.xlsx)":
                                    zip_data = excel_to_bytes_multi(dfs, file_prefix)
                                    mime_type = "application/zip"
                                    file_ext = "zip"
                                    download_filename = f"{file_prefix}_打包文件.zip"
                                else:
                                    # CSV格式打包
                                    zip_buffer = BytesIO()
                                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                                        for i, split_df in enumerate(dfs, 1):
                                            csv_buffer = StringIO()
                                            split_df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
                                            csv_buffer.seek(0)
                                            zip_file.writestr(f'{file_prefix}_{i:04d}.csv', csv_buffer.getvalue())
                                    zip_buffer.seek(0)
                                    zip_data = zip_buffer.getvalue()
                                    mime_type = "application/zip"
                                    file_ext = "zip"
                                    download_filename = f"{file_prefix}_打包文件.zip"
                                
                                st.session_state.split_result = {
                                    'zip_data': zip_data,
                                    'filename': download_filename,
                                    'mime_type': mime_type,
                                    'split_count': split_count
                                }
                                
                                st.markdown("""
                                <div class="success-cute">
                                    ✅ 文件拆分完成！
                                </div>
                                """, unsafe_allow_html=True)
                            
                            except Exception as e:
                                st.markdown(f"""
                                <div class="error-cute">
                                    ❌ 拆分失败：{str(e)}
                                </div>
                                """, unsafe_allow_html=True)
                
                with col_clear:
                    if st.button("🧹 清空数据", use_container_width=True):
                        st.session_state.split_df = None
                        st.session_state.split_result = None
                        st.rerun()
                
                # 显示下载按钮
                if st.session_state.split_result:
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown('<div class="potato-card"><div class="potato-card-header">📥 下载拆分文件</div></div>', unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="background: #E8F5E9; padding: 1rem; border-radius: 12px; margin: 1rem 0; text-align: center;">
                        <div style="color: #2E7D32; font-weight: 600; font-size: 1.1rem;">
                            🎉 成功生成 {st.session_state.split_result['split_count']} 个文件
                        </div>
                        <div style="color: #006400; margin-top: 0.5rem;">
                            点击下方按钮下载ZIP打包文件
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.download_button(
                        label="📥 下载打包文件",
                        data
