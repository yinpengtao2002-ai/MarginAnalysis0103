"""
单车边际变动归因分析 - Unit Margin Attribution Analysis
投行风格交互式BI大屏应用 - PVM Effect Analysis
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import StringIO

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="单车边际变动归因分析",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== Anthropic/Claude 品牌风格 CSS ====================
st.markdown("""
<style>
    /* 导入 Google 字体 - Anthropic 风格 */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Lora:wght@400;500;600&display=swap');
    
    /* Anthropic 品牌色彩变量 */
    :root {
        --bg-primary: #faf9f5;
        --bg-card: #ffffff;
        --text-primary: #141413;
        --text-secondary: #b0aea5;
        --accent-orange: #d97757;
        --accent-blue: #6a9bcc;
        --accent-green: #788c5d;
        --border-light: #e8e6dc;
        --shadow-soft: 0 4px 20px rgba(20, 20, 19, 0.06);
        --shadow-hover: 0 8px 30px rgba(217, 119, 87, 0.12);
    }
    
    /* 全局背景 - 温暖奶油色 */
    .stApp {
        background: var(--bg-primary);
        font-family: 'Lora', Georgia, serif;
    }
    
    /* 主标题容器 */
    .title-container {
        text-align: center;
        padding: 1.5rem 0 1.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    /* 底部装饰线 */
    .title-container::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 400px;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-light), transparent);
    }
    
    /* 主标题样式 - Anthropic 渐变 */
    .main-header {
        font-size: 3.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--accent-orange) 0%, var(--accent-blue) 50%, var(--accent-green) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 0.5rem 0;
        letter-spacing: 0.08em;
        font-family: 'Poppins', Arial, sans-serif;
    }
    
    /* 标题光晕效果 */
    .title-glow {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 500px;
        height: 120px;
        background: radial-gradient(ellipse, rgba(217, 119, 87, 0.08) 0%, transparent 70%);
        pointer-events: none;
        z-index: -1;
    }
    
    /* 副标题 */
    .sub-header {
        text-align: center;
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        letter-spacing: 0.25em;
        font-weight: 400;
        font-family: 'Poppins', Arial, sans-serif;
    }
    
    /* 标题装饰区 */
    .title-decoration {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .deco-line {
        width: 60px;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent-orange));
        border-radius: 1px;
    }
    
    .deco-line.right {
        background: linear-gradient(90deg, var(--accent-orange), transparent);
    }
    
    .deco-icon {
        font-size: 1.2rem;
        color: var(--accent-orange);
        animation: rotate 8s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* 标题标签 */
    .title-tags {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5rem;
        margin-top: 1.2rem;
        flex-wrap: wrap;
    }
    
    .tag {
        display: inline-block;
        padding: 0.35rem 0.9rem;
        background: linear-gradient(135deg, rgba(217, 119, 87, 0.08), rgba(106, 155, 204, 0.08));
        border: 1px solid var(--border-light);
        border-radius: 20px;
        font-size: 0.75rem;
        color: var(--text-secondary);
        font-family: 'Poppins', Arial, sans-serif;
        font-weight: 500;
        letter-spacing: 0.05em;
        transition: all 0.3s ease;
    }
    
    .tag:hover {
        border-color: var(--accent-orange);
        color: var(--accent-orange);
        background: rgba(217, 119, 87, 0.05);
    }
    
    .tag-dot {
        color: var(--border-light);
        font-size: 0.5rem;
    }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background: var(--bg-card);
        border-right: 1px solid var(--border-light);
    }
    
    /* 侧边栏展开按钮 */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        color: var(--accent-orange) !important;
    }
    
    button[kind="headerNoPadding"] {
        display: flex !important;
        visibility: visible !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: var(--text-primary);
        font-weight: 600;
        letter-spacing: 0.05em;
        border-left: 3px solid var(--accent-orange);
        padding-left: 0.8rem;
        margin-left: -0.5rem;
        font-family: 'Poppins', Arial, sans-serif;
    }
    
    /* 指标卡片 - 白色卡片风格 */
    [data-testid="stMetric"] {
        background: var(--bg-card);
        border: 1px solid var(--border-light);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: var(--shadow-soft);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover);
        border-color: rgba(217, 119, 87, 0.3);
    }
    
    [data-testid="stMetric"] label {
        color: var(--text-secondary) !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-family: 'Poppins', Arial, sans-serif;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        font-family: 'Poppins', Arial, sans-serif;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        font-size: 0.9rem !important;
    }
    
    /* 图表容器 */
    .chart-section {
        background: var(--bg-card);
        border: 1px solid var(--border-light);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-soft);
    }
    
    /* 子标题样式 */
    h3 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em;
        padding-bottom: 0.6rem;
        border-bottom: 2px solid var(--border-light);
        margin-bottom: 1rem !important;
        font-family: 'Poppins', Arial, sans-serif;
    }
    
    /* 信息提示框 */
    .stAlert {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 12px !important;
        border-left: 4px solid var(--accent-blue) !important;
    }
    
    /* 展开器 */
    .streamlit-expanderHeader {
        background: var(--bg-primary) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-family: 'Poppins', Arial, sans-serif;
    }
    
    /* 数据表格 */
    .stDataFrame {
        background: var(--bg-card) !important;
        border-radius: 10px !important;
        border: 1px solid var(--border-light) !important;
    }
    
    /* 分割线 */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, var(--border-light), transparent) !important;
        margin: 2rem 0 !important;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: var(--accent-orange);
        color: white;
        border: none;
        border-radius: 9999px;
        font-weight: 600;
        letter-spacing: 0.05em;
        padding: 0.6rem 1.8rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(217, 119, 87, 0.25);
        font-family: 'Poppins', Arial, sans-serif;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(217, 119, 87, 0.35);
        background: #c56646;
    }
    
    /* 下拉框 */
    .stSelectbox > div > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }
    
    /* Radio按钮 */
    .stRadio > div {
        background: var(--bg-primary);
        border-radius: 10px;
        padding: 0.8rem;
        border: 1px solid var(--border-light);
    }
    
    /* 成功提示 */
    .stSuccess {
        background: rgba(120, 140, 93, 0.1) !important;
        border: 1px solid rgba(120, 140, 93, 0.3) !important;
        border-left: 4px solid var(--accent-green) !important;
    }
    
    /* 文件上传器 */
    .stFileUploader {
        background: var(--bg-card);
        border: 2px dashed var(--border-light);
        border-radius: 14px;
        padding: 1.2rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: var(--accent-orange);
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 滚动条美化 */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-light);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-secondary);
    }
    
    /* 选中文本颜色 */
    ::selection {
        background: rgba(217, 119, 87, 0.2);
        color: var(--text-primary);
    }
</style>
""", unsafe_allow_html=True)


# ==================== Session State 初始化 ====================
# 下钻顺序配置（支持最多5个维度，可选择"无"跳过）
if 'drill_order' not in st.session_state:
    st.session_state.drill_order = ['Dim_A', 'Dim_B', 'Dim_C']  # 默认3个维度
# 维度选择状态 - 使用字典存储各维度的选择值
if 'selected_dims' not in st.session_state:
    st.session_state.selected_dims = {
        'Dim_A': None, 'Dim_B': None, 'Dim_C': None,
        'Dim_D': None, 'Dim_E': None
    }
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'df' not in st.session_state:
    st.session_state.df = None

# 用户自定义维度名称（Session State存储）
if 'custom_dim_names' not in st.session_state:
    st.session_state.custom_dim_names = {
        'Dim_A': '大区',
        'Dim_B': '国家', 
        'Dim_C': '车型',
        'Dim_D': '燃油品类',
        'Dim_E': '品牌'
    }

# 所有可用维度（英文列名）
ALL_DIMENSIONS = ['Dim_A', 'Dim_B', 'Dim_C', 'Dim_D', 'Dim_E']

# 获取当前维度显示名称的函数
def get_dim_names():
    return st.session_state.custom_dim_names.copy()

# 维度图标映射（基于维度顺序）
DIM_ICONS = {
    'Dim_A': '🌍',
    'Dim_B': '🏳️',
    'Dim_C': '🚗',
    'Dim_D': '🏷️',
    'Dim_E': '🏢'
}


# ==================== 示例数据生成 ====================
def generate_demo_data():
    """生成示例数据用于演示 PVM 归因分析"""
    data = [
        # 2025-01 基期数据
        # 亚太区
        {'Month': '2025-01', 'Dim_A': '亚太区', 'Dim_B': '中国', 'Dim_C': 'SUV-旗舰', 'Sales Volume': 5000, 'Total Margin': 15000000},
        {'Month': '2025-01', 'Dim_A': '亚太区', 'Dim_B': '中国', 'Dim_C': 'Sedan-经典', 'Sales Volume': 3500, 'Total Margin': 7000000},
        {'Month': '2025-01', 'Dim_A': '亚太区', 'Dim_B': '日本', 'Dim_C': 'SUV-旗舰', 'Sales Volume': 2000, 'Total Margin': 6400000},
        {'Month': '2025-01', 'Dim_A': '亚太区', 'Dim_B': '日本', 'Dim_C': 'EV-新能源', 'Sales Volume': 1500, 'Total Margin': 5250000},
        # 欧洲区
        {'Month': '2025-01', 'Dim_A': '欧洲区', 'Dim_B': '德国', 'Dim_C': 'SUV-旗舰', 'Sales Volume': 3000, 'Total Margin': 10500000},
        {'Month': '2025-01', 'Dim_A': '欧洲区', 'Dim_B': '德国', 'Dim_C': 'Sedan-经典', 'Sales Volume': 2500, 'Total Margin': 5500000},
        {'Month': '2025-01', 'Dim_A': '欧洲区', 'Dim_B': '法国', 'Dim_C': 'EV-新能源', 'Sales Volume': 1800, 'Total Margin': 5940000},
        # 美洲区
        {'Month': '2025-01', 'Dim_A': '美洲区', 'Dim_B': '美国', 'Dim_C': 'SUV-旗舰', 'Sales Volume': 4000, 'Total Margin': 14000000},
        {'Month': '2025-01', 'Dim_A': '美洲区', 'Dim_B': '美国', 'Dim_C': 'Pickup-皮卡', 'Sales Volume': 2800, 'Total Margin': 8400000},
        {'Month': '2025-01', 'Dim_A': '美洲区', 'Dim_B': '巴西', 'Dim_C': 'Sedan-经典', 'Sales Volume': 1200, 'Total Margin': 1800000},
        
        # 2025-02 当期数据 (包含结构变化和费率变化)
        # 亚太区 - 中国SUV增长，单车边际提升; 日本EV占比提升
        {'Month': '2025-02', 'Dim_A': '亚太区', 'Dim_B': '中国', 'Dim_C': 'SUV-旗舰', 'Sales Volume': 6200, 'Total Margin': 19840000},  # 量+24%, 单车边际+6.7%
        {'Month': '2025-02', 'Dim_A': '亚太区', 'Dim_B': '中国', 'Dim_C': 'Sedan-经典', 'Sales Volume': 3200, 'Total Margin': 6080000},  # 量-8.6%, 单车边际-5%
        {'Month': '2025-02', 'Dim_A': '亚太区', 'Dim_B': '日本', 'Dim_C': 'SUV-旗舰', 'Sales Volume': 1800, 'Total Margin': 5580000},  # 量-10%, 单车边际-3%
        {'Month': '2025-02', 'Dim_A': '亚太区', 'Dim_B': '日本', 'Dim_C': 'EV-新能源', 'Sales Volume': 2200, 'Total Margin': 8140000},  # 量+47%, 单车边际+5.7%
        # 欧洲区 - 德国整体下滑，法国EV大增
        {'Month': '2025-02', 'Dim_A': '欧洲区', 'Dim_B': '德国', 'Dim_C': 'SUV-旗舰', 'Sales Volume': 2600, 'Total Margin': 8580000},  # 量-13%, 单车边际-5.7%
        {'Month': '2025-02', 'Dim_A': '欧洲区', 'Dim_B': '德国', 'Dim_C': 'Sedan-经典', 'Sales Volume': 2200, 'Total Margin': 4620000},  # 量-12%, 单车边际-4.5%
        {'Month': '2025-02', 'Dim_A': '欧洲区', 'Dim_B': '法国', 'Dim_C': 'EV-新能源', 'Sales Volume': 2800, 'Total Margin': 10080000},  # 量+56%, 单车边际+9%
        # 美洲区 - 美国皮卡需求旺，巴西新增SUV
        {'Month': '2025-02', 'Dim_A': '美洲区', 'Dim_B': '美国', 'Dim_C': 'SUV-旗舰', 'Sales Volume': 4200, 'Total Margin': 14700000},  # 量+5%
        {'Month': '2025-02', 'Dim_A': '美洲区', 'Dim_B': '美国', 'Dim_C': 'Pickup-皮卡', 'Sales Volume': 3500, 'Total Margin': 11200000},  # 量+25%, 单车边际+6.7%
        {'Month': '2025-02', 'Dim_A': '美洲区', 'Dim_B': '巴西', 'Dim_C': 'Sedan-经典', 'Sales Volume': 1000, 'Total Margin': 1400000},  # 量-17%, 单车边际-6.7%
        {'Month': '2025-02', 'Dim_A': '美洲区', 'Dim_B': '巴西', 'Dim_C': 'SUV-旗舰', 'Sales Volume': 800, 'Total Margin': 2000000},  # 新品
    ]
    return pd.DataFrame(data)


# ==================== 数据处理函数 ====================
def clean_numeric_column(series):
    """清理数值列，处理各种格式问题"""
    if series.dtype in ['int64', 'float64']:
        return series
    
    # 转换为字符串处理
    cleaned = series.astype(str)
    # 移除千分位逗号、空格、货币符号等
    cleaned = cleaned.str.replace(',', '', regex=False)
    cleaned = cleaned.str.replace(' ', '', regex=False)
    cleaned = cleaned.str.replace('¥', '', regex=False)
    cleaned = cleaned.str.replace('$', '', regex=False)
    cleaned = cleaned.str.replace('￥', '', regex=False)
    # 处理空值
    cleaned = cleaned.replace(['', 'nan', 'None', 'null', '-'], '0')
    # 转换为数值
    return pd.to_numeric(cleaned, errors='coerce').fillna(0)


def load_data(uploaded_file=None, pasted_data=None):
    """加载数据：支持CSV和XLSX文件上传或手动粘贴"""
    try:
        if uploaded_file is not None:
            # 根据文件类型选择读取方式
            file_name = uploaded_file.name.lower()
            if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                try:
                    df = pd.read_excel(uploaded_file, engine='openpyxl')
                except ImportError:
                    st.error("请安装openpyxl库: pip install openpyxl")
                    return None
            else:
                df = pd.read_csv(uploaded_file)
        elif pasted_data:
            df = pd.read_csv(StringIO(pasted_data))
        else:
            return None
        
        # 移除完全空的行
        df = df.dropna(how='all')
        
        # 标准化列名（去除空格）
        df.columns = [str(col).strip() for col in df.columns]
        
        # 列名映射（只支持标准格式）
        column_mapping = {
            # 月份
            '月份': 'Month', 'month': 'Month', 'Month': 'Month',
            # 维度列（只支持Dim_A/B/C/D/E格式）
            'Dim_A': 'Dim_A', 'dim_a': 'Dim_A', 'DimA': 'Dim_A',
            'Dim_B': 'Dim_B', 'dim_b': 'Dim_B', 'DimB': 'Dim_B',
            'Dim_C': 'Dim_C', 'dim_c': 'Dim_C', 'DimC': 'Dim_C',
            'Dim_D': 'Dim_D', 'dim_d': 'Dim_D', 'DimD': 'Dim_D',
            'Dim_E': 'Dim_E', 'dim_e': 'Dim_E', 'DimE': 'Dim_E',
            # 销量
            '销量': 'Sales Volume', 'sales volume': 'Sales Volume', 
            'salesvolume': 'Sales Volume', 'Sales Volume': 'Sales Volume',
            'SalesVolume': 'Sales Volume', 'sales_volume': 'Sales Volume',
            # 边际总额
            '边际总额': 'Total Margin', 'total margin': 'Total Margin', 
            'totalmargin': 'Total Margin', 'Total Margin': 'Total Margin',
            'TotalMargin': 'Total Margin', 'total_margin': 'Total Margin'
        }
        df.columns = [column_mapping.get(col.strip(), col.strip()) for col in df.columns]
        
        # 检查必要列（只需要月份、至少一个维度、销量和边际）
        required_cols = ['Month', 'Sales Volume', 'Total Margin']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        # 检查是否至少有一个维度列
        dim_cols = [col for col in ['Dim_A', 'Dim_B', 'Dim_C', 'Dim_D', 'Dim_E'] if col in df.columns]
        if not dim_cols:
            st.error("缺少维度列: 请至少包含Dim_A")
            st.info(f"当前列名: {list(df.columns)}")
            return None
        
        if missing_cols:
            st.error(f"缺少必要列: {missing_cols}")
            st.info(f"当前列名: {list(df.columns)}")
            return None
        
        # 强制转换数值列为正确的数值类型
        df['Sales Volume'] = clean_numeric_column(df['Sales Volume'])
        df['Total Margin'] = clean_numeric_column(df['Total Margin'])
        
        # 只移除销量和边际都为0的行（可能是汇总行或标题行）
        # 保留有margin但没有销量的行
        df = df[(df['Sales Volume'] != 0) | (df['Total Margin'] != 0)]
        
        # 转换维度列为字符串
        df['Month'] = df['Month'].astype(str).str.strip()
        for dim in dim_cols:
            df[dim] = df[dim].astype(str).str.strip()
        
        if df.empty:
            st.error("数据清理后为空，请检查数据格式")
            return None
        
        return df
    except Exception as e:
        st.error(f"数据加载失败: {e}")
        import traceback
        st.code(traceback.format_exc())
        return None


def aggregate_data(df, group_cols, month):
    """按维度聚合数据并计算单车边际"""
    month_data = df[df['Month'] == month].copy()
    if month_data.empty:
        return pd.DataFrame()
    
    agg_df = month_data.groupby(group_cols).agg({
        'Sales Volume': 'sum',
        'Total Margin': 'sum'
    }).reset_index()
    
    # 安全计算单车边际，避免除以零
    agg_df['Unit Margin'] = agg_df.apply(
        lambda row: row['Total Margin'] / row['Sales Volume'] if row['Sales Volume'] != 0 else 0, 
        axis=1
    )
    return agg_df


def calculate_global_metrics(df, month):
    """计算全球指标"""
    month_data = df[df['Month'] == month]
    total_vol = month_data['Sales Volume'].sum()
    total_margin = month_data['Total Margin'].sum()
    avg_margin = total_margin / total_vol if total_vol > 0 else 0
    return total_vol, total_margin, avg_margin


def calculate_atomic_pvm_effects(df, base_month, curr_month, global_vol_curr, global_vol_base, global_avg_margin_base):
    """
    计算原子PVM效应（最细颗粒度）
    
    逻辑：
    1. 识别数据中所有存在的维度 (Dim_A ... Dim_E)，组合成"原子"
    2. 在原子层级计算 Mix 和 Rate 效应
    3. 特殊处理新品和停产品
    """
    # 1. 识别所有可用维度
    all_dims = [c for c in ['Dim_A', 'Dim_B', 'Dim_C', 'Dim_D', 'Dim_E'] if c in df.columns]
    
    if not all_dims:
        return pd.DataFrame()

    # 2. 分别提取基期和当期数据并按所有维度聚合
    base_df = df[df['Month'] == base_month].groupby(all_dims).agg({
        'Sales Volume': 'sum', 'Total Margin': 'sum'
    }).reset_index()
    curr_df = df[df['Month'] == curr_month].groupby(all_dims).agg({
        'Sales Volume': 'sum', 'Total Margin': 'sum'
    }).reset_index()
    
    # 3. 合并数据
    merged = pd.merge(
        base_df, curr_df, on=all_dims, how='outer', suffixes=('_Base', '_Curr')
    ).fillna(0)
    
    # 4. 计算原子层级的权重和单车边际
    # 权重是相对于【全球】总销量的
    merged['Weight_Base'] = merged['Sales Volume_Base'] / global_vol_base if global_vol_base > 0 else 0
    merged['Weight_Curr'] = merged['Sales Volume_Curr'] / global_vol_curr if global_vol_curr > 0 else 0
    
    merged['Unit_Margin_Base'] = merged.apply(lambda x: x['Total Margin_Base'] / x['Sales Volume_Base'] if x['Sales Volume_Base'] != 0 else 0, axis=1)
    merged['Unit_Margin_Curr'] = merged.apply(lambda x: x['Total Margin_Curr'] / x['Sales Volume_Curr'] if x['Sales Volume_Curr'] != 0 else 0, axis=1)
    
    # 5. PVM 计算逻辑
    # 识别新品和停产品
    is_new = (merged['Sales Volume_Base'] == 0) & (merged['Sales Volume_Curr'] > 0)
    is_disc = (merged['Sales Volume_Curr'] == 0) & (merged['Sales Volume_Base'] > 0)
    is_exist = ~is_new & ~is_disc
    
    merged['Mix_Effect'] = 0.0
    merged['Rate_Effect'] = 0.0
    
    # === 现有产品 ===
    # Mix: (Weight_Curr - Weight_Base) * (Unit_Margin_Base - Global_Avg_Margin_Base)
    # Rate: Weight_Curr * (Unit_Margin_Curr - Unit_Margin_Base)
    merged.loc[is_exist, 'Mix_Effect'] = (merged.loc[is_exist, 'Weight_Curr'] - merged.loc[is_exist, 'Weight_Base']) * (merged.loc[is_exist, 'Unit_Margin_Base'] - global_avg_margin_base)
    merged.loc[is_exist, 'Rate_Effect'] = merged.loc[is_exist, 'Weight_Curr'] * (merged.loc[is_exist, 'Unit_Margin_Curr'] - merged.loc[is_exist, 'Unit_Margin_Base'])
    
    # === 新品 (0 -> N) ===
    # Mix: Weight_Curr * (Unit_Margin_Curr - Global_Avg_Margin_Base)
    # Rate: 0
    merged.loc[is_new, 'Mix_Effect'] = merged.loc[is_new, 'Weight_Curr'] * (merged.loc[is_new, 'Unit_Margin_Curr'] - global_avg_margin_base)
    merged.loc[is_new, 'Rate_Effect'] = 0
    
    # === 停产品 (N -> 0) ===
    # Mix: (0 - Weight_Base) * (Unit_Margin_Base - Global_Avg_Margin_Base)
    # Rate: 0
    merged.loc[is_disc, 'Mix_Effect'] = (0 - merged.loc[is_disc, 'Weight_Base']) * (merged.loc[is_disc, 'Unit_Margin_Base'] - global_avg_margin_base)
    merged.loc[is_disc, 'Rate_Effect'] = 0
    
    return merged


def aggregate_pvm_effects(atomic_df, group_dim):
    """
    将原子层级的PVM效应汇总到指定维度
    """
    # 按指定维度聚合
    agg = atomic_df.groupby(group_dim).agg({
        'Sales Volume_Base': 'sum',
        'Sales Volume_Curr': 'sum',
        'Total Margin_Base': 'sum',
        'Total Margin_Curr': 'sum',
        'Mix_Effect': 'sum',
        'Rate_Effect': 'sum'
    }).reset_index()
    
    # 重命名以适配现有的显示逻辑
    agg = agg.rename(columns={
        'Sales Volume_Base': 'Vol_Base',
        'Sales Volume_Curr': 'Vol_Curr',
        'Mix_Effect': 'Relative_Mix_Effect',  # 保持列名兼容
    })
    
    # 计算展示用的平均单车边际 (仅供参考，不参与PVM计算)
    agg['Margin_Unit_Base'] = agg.apply(lambda x: x['Total Margin_Base'] / x['Vol_Base'] if x['Vol_Base'] != 0 else 0, axis=1)
    agg['Margin_Unit_Curr'] = agg.apply(lambda x: x['Total Margin_Curr'] / x['Vol_Curr'] if x['Vol_Curr'] != 0 else 0, axis=1)
    
    # 总贡献
    agg['Total_Contribution'] = agg['Relative_Mix_Effect'] + agg['Rate_Effect']
    
    return agg


def prepare_display_dataframe(effects_df, dimension_col, total_vol_base, total_vol_curr, 
                               total_margin_base=None, total_margin_curr=None, is_global=False):
    """
    准备用于展示的DataFrame，添加销量占比列和总计行
    
    Args:
        effects_df: PVM效应计算结果
        dimension_col: 维度列名 (Region/Country/Model)
        total_vol_base: 用于计算占比的基期总销量
        total_vol_curr: 用于计算占比的当期总销量
        total_margin_base: 基期总边际（用于计算总计行的单车边际）
        total_margin_curr: 当期总边际（用于计算总计行的单车边际）
        is_global: 是否是全球贡献表格
    """
    df = effects_df.copy()
    
    # 计算销量占比
    df['Weight_Base_Pct'] = (df['Vol_Base'] / total_vol_base * 100) if total_vol_base > 0 else 0
    df['Weight_Curr_Pct'] = (df['Vol_Curr'] / total_vol_curr * 100) if total_vol_curr > 0 else 0
    
    # 按当期销量从高到低排序（在添加总计行之前）
    df = df.sort_values('Vol_Curr', ascending=False).reset_index(drop=True)
    
    # 创建总计行
    total_row = {
        dimension_col: '总计',
        'Vol_Base': df['Vol_Base'].sum(),
        'Weight_Base_Pct': df['Weight_Base_Pct'].sum(),
        'Vol_Curr': df['Vol_Curr'].sum(),
        'Weight_Curr_Pct': df['Weight_Curr_Pct'].sum(),
        'Relative_Mix_Effect': df['Relative_Mix_Effect'].sum(),
        'Rate_Effect': df['Rate_Effect'].sum(),
        'Total_Contribution': df['Total_Contribution'].sum()
    }
    
    # 计算总计行的单车边际
    if total_margin_base is not None and total_margin_curr is not None:
        total_row['Margin_Unit_Base'] = total_margin_base / df['Vol_Base'].sum() if df['Vol_Base'].sum() > 0 else 0
        total_row['Margin_Unit_Curr'] = total_margin_curr / df['Vol_Curr'].sum() if df['Vol_Curr'].sum() > 0 else 0
    else:
        # 使用加权平均
        total_row['Margin_Unit_Base'] = (df['Vol_Base'] * df['Margin_Unit_Base']).sum() / df['Vol_Base'].sum() if df['Vol_Base'].sum() > 0 else 0
        total_row['Margin_Unit_Curr'] = (df['Vol_Curr'] * df['Margin_Unit_Curr']).sum() / df['Vol_Curr'].sum() if df['Vol_Curr'].sum() > 0 else 0
    
    # 添加总计行（总计行始终在最后）
    df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)
    
    return df


def create_waterfall_chart(data, dimension_col, title, base_margin, curr_margin, color_scheme='gold'):
    """创建投行风格瀑布图 - 有头有尾，灵活Y轴"""
    # 先按绝对值选出Top 10，再按"先负后正"排列
    sorted_by_abs = data.sort_values('Total_Contribution', key=abs, ascending=False)
    
    if len(sorted_by_abs) > 10:
        top_10 = sorted_by_abs.head(10).copy()
        others_sum = sorted_by_abs.iloc[10:]['Total_Contribution'].sum()
        
        # 在top10内部按先负后正排序（即按值从小到大排）
        top_10_sorted = top_10.sort_values('Total_Contribution', ascending=True)
        
        labels = ['基期单车边际'] + top_10_sorted[dimension_col].tolist() + ['其他', '当期单车边际']
        values = [base_margin] + top_10_sorted['Total_Contribution'].tolist() + [others_sum, 0]
        measures = ['absolute'] + ['relative'] * 11 + ['total']
    else:
        # 按先负后正排序
        sorted_data = sorted_by_abs.sort_values('Total_Contribution', ascending=True)
        
        labels = ['基期单车边际'] + sorted_data[dimension_col].tolist() + ['当期单车边际']
        values = [base_margin] + sorted_data['Total_Contribution'].tolist() + [0]
        measures = ['absolute'] + ['relative'] * len(sorted_data) + ['total']
    
    # Anthropic 品牌颜色方案
    color_schemes = {
        'claude': {
            'increasing': '#788c5d',   # Anthropic Green
            'decreasing': '#d97757',   # Anthropic Orange  
            'total': '#6a9bcc',        # Anthropic Blue
            'base': '#b0aea5'          # Anthropic Gray
        },
        'warm': {
            'increasing': '#788c5d',
            'decreasing': '#c56646',
            'total': '#5a89b8',
            'base': '#9a988f'
        },
        'soft': {
            'increasing': '#8fa370',
            'decreasing': '#e08060',
            'total': '#7aaad4',
            'base': '#c0beb5'
        }
    }
    colors = color_schemes.get(color_scheme, color_schemes['claude'])
    
    # 计算Y轴范围 - 灵活调整起始位置
    min_margin = min(base_margin, curr_margin)
    max_margin = max(base_margin, curr_margin)
    delta = abs(curr_margin - base_margin)
    
    # 计算中间相对值的累积范围
    cumulative = base_margin
    min_cumulative = base_margin
    max_cumulative = base_margin
    for i, v in enumerate(values[1:-1]):  # 跳过第一个和最后一个
        cumulative += v
        min_cumulative = min(min_cumulative, cumulative)
        max_cumulative = max(max_cumulative, cumulative)
    
    # Y轴范围：给差异留出足够空间显示变化，同时正确处理负数
    data_range = max_cumulative - min_cumulative
    padding = max(abs(delta) * 1.5, data_range * 0.3, 100)  # 确保有足够的padding
    
    y_range_min = min(min_margin, min_cumulative) - padding
    y_range_max = max(max_margin, max_cumulative) + padding * 1.5  # 上方多留空间给标签
    
    # 如果所有数据都是正的，且范围允许，可以从0开始
    if min_margin > 0 and min_cumulative > 0:
        # 检查是否适合从0开始（不会导致数据显示过小）
        if min(min_margin, min_cumulative) > (max(max_margin, max_cumulative) * 0.3):
            # 数据不适合从0开始，保持动态范围
            pass
        else:
            # 可以考虑从0开始
            y_range_min = max(0, y_range_min)
    
    fig = go.Figure()
    
    # 生成文本标签 - 首尾显示实际值，中间显示差异值
    text_labels = []
    for i, v in enumerate(values):
        if i == 0:  # 基期
            text_labels.append(f"¥{base_margin:,.0f}")
        elif i == len(values) - 1:  # 当期
            text_labels.append(f"¥{curr_margin:,.0f}")
        else:  # 中间的相对值
            text_labels.append(f"{v:+,.0f}")
    
    # 添加瀑布图
    fig.add_trace(go.Waterfall(
        name="",
        orientation="v",
        measure=measures,
        x=labels,
        y=values,
        textposition="outside",
        text=text_labels,
        textfont=dict(size=13, color='#141413', family='Poppins'),
        increasing={"marker": {"color": colors['increasing'], "line": {"color": colors['increasing'], "width": 1}}},
        decreasing={"marker": {"color": colors['decreasing'], "line": {"color": colors['decreasing'], "width": 1}}},
        totals={"marker": {"color": colors['total'], "line": {"color": colors['total'], "width": 2}}},
        connector={"line": {"color": "rgba(176, 174, 165, 0.3)", "width": 1.5, "dash": "dot"}},
    ))
    
    fig.update_layout(
        title={
            'text': f'<b>{title}</b>',
            'font': {'size': 18, 'color': '#141413', 'family': 'Poppins'},
            'x': 0.5,
            'xanchor': 'center'
        },
        showlegend=False,
        height=520,
        margin=dict(l=80, r=80, t=120, b=100),
        plot_bgcolor='rgba(250, 249, 245, 0)',
        paper_bgcolor='rgba(250, 249, 245, 0)',
        xaxis=dict(
            tickangle=-25,
            tickfont=dict(size=12, color='#b0aea5', family='Poppins'),
            gridcolor='rgba(232, 230, 220, 0.5)',
            linecolor='#e8e6dc',
            showline=True
        ),
        yaxis=dict(
            title=dict(text='单车边际 (¥)', font=dict(size=13, color='#b0aea5')),
            gridcolor='rgba(232, 230, 220, 0.5)',
            tickfont=dict(size=11, color='#b0aea5'),
            tickformat=',.0f',
            linecolor='#e8e6dc',
            showline=True,
            range=[y_range_min, y_range_max],
            zeroline=False
        ),
        hoverlabel=dict(
            bgcolor='rgba(255, 255, 255, 0.98)',
            bordercolor='#d97757',
            font=dict(size=13, color='#141413', family='Poppins')
        )
    )
    
    # 添加注释 - 变动金额
    delta_val = curr_margin - base_margin
    pct_change = (delta_val / base_margin * 100) if base_margin != 0 else 0
    delta_color = '#788c5d' if delta_val >= 0 else '#d97757'
    
    fig.add_annotation(
        x=0.5,
        y=1.08,
        xref='paper',
        yref='paper',
        text=f'<b>变动: ¥{delta_val:+,.0f}</b>  <span style="color: {delta_color}">({pct_change:+.2f}%)</span>',
        showarrow=False,
        font=dict(size=15, color=delta_color, family='Poppins'),
        bgcolor='rgba(255, 255, 255, 0.95)',
        bordercolor='#e8e6dc',
        borderwidth=1,
        borderpad=10
    )
    
    return fig


# ==================== 主界面 ====================
st.markdown("""
<div class="title-container">
    <div class="title-glow"></div>
    <div class="title-decoration">
        <span class="deco-line left"></span>
        <span class="deco-icon">◈</span>
        <span class="deco-line right"></span>
    </div>
    <h1 class="main-header">单车边际变动归因分析</h1>
    <p class="sub-header">Unit Margin Attribution Analysis</p>
    <div class="title-tags">
        <span class="tag">PVM 归因</span>
        <span class="tag-dot">·</span>
        <span class="tag">结构效应</span>
        <span class="tag-dot">·</span>
        <span class="tag">费率效应</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== 侧边栏 ====================
with st.sidebar:
    # 数据中心（放在最上面）
    if st.session_state.data_loaded:
        with st.expander("📁 数据中心", expanded=False):
            uploaded_file = st.file_uploader("上传CSV或Excel文件", type=['csv', 'xlsx', 'xls'], key="uploader_loaded")
            if uploaded_file:
                new_df = load_data(uploaded_file=uploaded_file)
                if new_df is not None:
                    st.session_state.df = new_df
                    st.success("✅ 数据已加载")
        # 使用session_state中的df
        df = st.session_state.df
    else:
        st.markdown("## 📁 数据中心")
        uploaded_file = st.file_uploader("上传CSV或Excel文件", type=['csv', 'xlsx', 'xls'])
        if uploaded_file:
            df = load_data(uploaded_file=uploaded_file)
            if df is not None:
                st.session_state.df = df
                st.success("✅ 数据已加载")
                st.session_state.data_loaded = True
                st.rerun()
        else:
            df = None
        
        # 示例数据按钮
        st.markdown("---")
        st.caption("或者体验示例数据")
        if st.button("📊 加载示例数据", use_container_width=True, type="primary"):
            df = generate_demo_data()
            st.session_state.df = df
            st.session_state.data_loaded = True
            st.success("✅ 示例数据已加载")
            st.rerun()
        st.markdown("---")
    
    # 维度配置
    if st.session_state.data_loaded:
        with st.expander("⚙️ 维度配置", expanded=False):
            st.caption("设置各维度的显示名称（修改后自动更新）")
            for dim in ALL_DIMENSIONS:
                new_value = st.text_input(
                    f"{dim}",
                    value=st.session_state.custom_dim_names.get(dim, dim),
                    key=f"dim_name_{dim}_loaded"
                )
                if new_value != st.session_state.custom_dim_names.get(dim):
                    st.session_state.custom_dim_names[dim] = new_value
                    st.rerun()
    else:
        st.markdown("## ⚙️ 维度配置")
        st.caption("设置各维度的显示名称")
        dim_names = get_dim_names()
        new_dim_names = {}
        for dim in ALL_DIMENSIONS:
            new_dim_names[dim] = st.text_input(
                f"{dim}",
                value=dim_names.get(dim, dim),
                key=f"dim_name_{dim}"
            )
        if new_dim_names != st.session_state.custom_dim_names:
            st.session_state.custom_dim_names = new_dim_names
            st.rerun()
    
    if df is not None:
        st.session_state.data_loaded = True
        st.markdown("---")
        
        # 期间选择
        st.markdown("## 📅 分析期间")
        months = sorted(df['Month'].unique().tolist())
        
        if len(months) >= 2:
            base_month = st.selectbox("基期", months, index=0)
            curr_month = st.selectbox("当期", months, index=min(1, len(months)-1))
        else:
            st.error("需要至少两个月份")
            st.stop()
        
        st.markdown("---")
        
        # 下钻顺序选择
        st.markdown("## 🔀 下钻顺序")
        st.caption('选择"无"可跳过该层级')
        
        # 获取当前维度名称
        dim_names = get_dim_names()
        
        # 检测数据中存在的维度列
        available_dims_in_data = [dim for dim in ALL_DIMENSIONS if dim in df.columns]
        
        dim_options_base = {dim: dim_names.get(dim, dim) for dim in available_dims_in_data}
        reverse_mapping = {v: k for k, v in dim_options_base.items()}
        
        # 获取当前下钻顺序
        current_order = st.session_state.drill_order
        
        # 5个层级选择框
        selected_dims_list = []
        
        for level in range(1, 6):
            # 排除已选的维度
            used_dims = [dim_names.get(d, d) for d in selected_dims_list]
            available_options = ['无'] + [v for v in dim_options_base.values() if v not in used_dims]
            
            # 如果没有可选的维度了（除了"无"），跳过
            if len(available_options) <= 1:
                break
            
            # 获取当前层级的默认值
            if level <= len(current_order):
                # 如果当前下钻顺序有这个层级，使用它的值
                current_dim = current_order[level - 1]
                current_dim_name = dim_names.get(current_dim, current_dim)
                if current_dim_name in available_options:
                    default_idx = available_options.index(current_dim_name)
                else:
                    # 当前维度不在可选列表中，选择"无"
                    default_idx = 0
            else:
                # 超出当前下钻顺序长度，默认选择"无"
                default_idx = 0
            
            selected = st.selectbox(
                f"{'①②③④⑤'[level-1]} 第{['一','二','三','四','五'][level-1]}层级",
                available_options,
                index=default_idx,
                key=f"drill_{level}"
            )
            
            if selected != '无':
                dim_eng = reverse_mapping.get(selected)
                if dim_eng:
                    selected_dims_list.append(dim_eng)
        
        # 构建新的下钻顺序（过滤掉"无"）
        new_order = selected_dims_list if selected_dims_list else ['Region', 'Country', 'Model']
        
        if new_order != st.session_state.drill_order:
            st.session_state.drill_order = new_order
            # 重置所有维度选择
            st.session_state.selected_dims = {dim: None for dim in ALL_DIMENSIONS}
            st.rerun()
        
        st.markdown("---")
        
        # 动态维度钻取
        st.markdown("## 🔍 维度钻取")
        st.caption("支持多选，留空表示全部")
        
        drill_order = st.session_state.drill_order
        
        # 根据下钻顺序动态生成筛选器
        df_filtered = df.copy()
        
        for i, dim in enumerate(drill_order):
            # 显示除最后一层外的所有维度筛选器（最后一层在主内容区作为明细显示）
            if i >= len(drill_order) - 1:
                break
            
            # 获取当前维度的可选值（基于已选择的上级维度筛选）
            available_values = sorted(df_filtered[dim].unique().tolist())
            
            # 获取当前选择（多选列表）
            current_selection = st.session_state.selected_dims.get(dim) or []
            # 确保current_selection是列表
            if not isinstance(current_selection, list):
                current_selection = [current_selection] if current_selection else []
            # 确保选择值在可选值中
            valid_selection = [v for v in current_selection if v in available_values]
            
            selected_values = st.multiselect(
                f"{DIM_ICONS.get(dim, '')} {dim_names.get(dim, dim)}",
                available_values,
                default=valid_selection,
                key=f"select_{dim}"
            )
            
            if selected_values:
                st.session_state.selected_dims[dim] = selected_values
                df_filtered = df_filtered[df_filtered[dim].isin(selected_values)]
            else:
                st.session_state.selected_dims[dim] = None
        
        # 重置按钮
        if st.button("🔄 重置筛选", use_container_width=True):
            st.session_state.selected_dims = {dim: None for dim in ALL_DIMENSIONS}
            st.rerun()


# ==================== 主要内容区域 ====================
if df is not None:
    # 计算全球指标
    global_vol_base, global_margin_base, global_avg_margin_base = calculate_global_metrics(df, base_month)
    global_vol_curr, global_margin_curr, global_avg_margin_curr = calculate_global_metrics(df, curr_month)
    total_diff = global_avg_margin_curr - global_avg_margin_base
    
    # 顶部指标卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label=f"📦 {base_month} 全球销量",
            value=f"{global_vol_base:,.0f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label=f"📦 {curr_month} 全球销量",
            value=f"{global_vol_curr:,.0f}",
            delta=f"{global_vol_curr - global_vol_base:+,.0f}"
        )
    
    with col3:
        st.metric(
            label=f"💎 {base_month} 单车边际",
            value=f"¥{global_avg_margin_base:,.0f}",
            delta=None
        )
    
    with col4:
        st.metric(
            label=f"💎 {curr_month} 单车边际",
            value=f"¥{global_avg_margin_curr:,.0f}",
            delta=f"¥{total_diff:+,.0f}"
        )
    
    st.markdown("---")
    
    # ==================== 动态维度图表 ====================
    # 根据下钻顺序依次显示三个维度的图表
    drill_order = st.session_state.drill_order
    color_schemes = ['claude', 'warm', 'soft']
    dim_names = get_dim_names()  # 获取当前维度名称配置
    
    for level, dim in enumerate(drill_order):
        dim_name = dim_names.get(dim, dim)
        dim_icon = DIM_ICONS.get(dim, '📊')
        
        st.subheader(f"{dim_icon} {dim_name}维度贡献分析")
        
        # 根据已选择的上级维度筛选数据
        df_level = df.copy()
        is_drilled = False
        drill_info_parts = []
        
        for prev_level in range(level):
            prev_dim = drill_order[prev_level]
            prev_selection = st.session_state.selected_dims.get(prev_dim)
            if prev_selection:
                # 支持多选：使用isin()筛选
                if isinstance(prev_selection, list):
                    df_level = df_level[df_level[prev_dim].isin(prev_selection)]
                    selection_text = ', '.join(prev_selection) if len(prev_selection) <= 3 else f"{len(prev_selection)}项"
                else:
                    df_level = df_level[df_level[prev_dim] == prev_selection]
                    selection_text = prev_selection
                is_drilled = True
                drill_info_parts.append(f"{dim_names.get(prev_dim, prev_dim)}: **{selection_text}**")
        
        if is_drilled:
            st.info(f"📍 已筛选 {' → '.join(drill_info_parts)}")
        
        if not df_level.empty:
            # 1. 计算当前视图范围（下钻上下文）的基准指标
            level_base_df = df_level[df_level['Month'] == base_month]
            level_curr_df = df_level[df_level['Month'] == curr_month]
            
            level_vol_base = level_base_df['Sales Volume'].sum()
            level_vol_curr = level_curr_df['Sales Volume'].sum()
            
            level_total_margin_base = level_base_df['Total Margin'].sum()
            level_total_margin_curr = level_curr_df['Total Margin'].sum()
            
            level_avg_margin_base = level_total_margin_base / level_vol_base if level_vol_base > 0 else 0
            level_avg_margin_curr = level_total_margin_curr / level_vol_curr if level_vol_curr > 0 else 0
            
            # 2. 计算原子PVM效应 (基于当前视图范围)
            # 所有的Mix/Rate计算都基于最细颗粒度，但权重是相对于当前视图总量的
            level_atomic_effects = calculate_atomic_pvm_effects(
                df_level, base_month, curr_month,
                level_vol_curr, level_vol_base, level_avg_margin_base
            )
            
            if not level_atomic_effects.empty:
                # 3. 聚合到当前显示维度
                effects = aggregate_pvm_effects(level_atomic_effects, dim)
                
                # 4. 创建瀑布图
                fig = create_waterfall_chart(
                    effects, dim,
                    f'{dim_name}贡献分解 (自底向上计算)',
                    level_avg_margin_base,
                    level_avg_margin_curr,
                    color_schemes[level % len(color_schemes)]
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # 5. 显示明细数据
                with st.expander(f"📋 {dim_name}明细数据"):
                    display_df = prepare_display_dataframe(
                        effects, dim,
                        level_vol_base,
                        level_vol_curr,
                        level_total_margin_base,
                        level_total_margin_curr
                    )
                    
                    display_cols = [dim, 'Vol_Base', 'Weight_Base_Pct', 'Vol_Curr', 'Weight_Curr_Pct',
                                   'Margin_Unit_Base', 'Margin_Unit_Curr',
                                   'Relative_Mix_Effect', 'Rate_Effect', 'Total_Contribution']
                                   
                    st.dataframe(
                        display_df[display_cols].rename(columns={
                            dim: dim_name,
                            'Vol_Base': '基期销量',
                            'Weight_Base_Pct': '基期占比%',
                            'Vol_Curr': '当期销量',
                            'Weight_Curr_Pct': '当期占比%',
                            'Margin_Unit_Base': '基期单车边际',
                            'Margin_Unit_Curr': '当期单车边际',
                            'Relative_Mix_Effect': '结构效应',
                            'Rate_Effect': '费率效应',
                            'Total_Contribution': '总贡献'
                        }).style.format({
                            '基期销量': '{:,.0f}',
                            '基期占比%': '{:.1f}%',
                            '当期销量': '{:,.0f}',
                            '当期占比%': '{:.1f}%',
                            '基期单车边际': '¥{:,.0f}',
                            '当期单车边际': '¥{:,.0f}',
                            '结构效应': '{:+,.0f}',
                            '费率效应': '{:+,.0f}',
                            '总贡献': '{:+,.0f}'
                        }),
                        use_container_width=True
                    )
                    
                    # 如果是下钻状态，显示对全球整体的影响 (即不重新计算权重，直接使用全球权重的原子效应)
                    if is_drilled:
                        st.markdown("---")
                        st.markdown("##### 🌐 对全球整体单车边际的贡献")
                        
                        # 重新计算基于全球视角的原子效应 (仅针对筛选出的数据)
                        global_context_atomic = calculate_atomic_pvm_effects(
                            df_level, base_month, curr_month,
                            global_vol_curr, global_vol_base, global_avg_margin_base
                        )
                        
                        if not global_context_atomic.empty:
                            global_effects = aggregate_pvm_effects(global_context_atomic, dim)
                            
                            global_display_df = prepare_display_dataframe(
                                global_effects, dim,
                                global_vol_base, global_vol_curr,
                                is_global=True
                            )
                            
                            st.dataframe(
                                global_display_df[display_cols].rename(columns={
                                    dim: dim_name,
                                    'Vol_Base': '基期销量',
                                    'Weight_Base_Pct': '基期占比%',
                                    'Vol_Curr': '当期销量',
                                    'Weight_Curr_Pct': '当期占比%',
                                    'Margin_Unit_Base': '基期单车边际',
                                    'Margin_Unit_Curr': '当期单车边际',
                                    'Relative_Mix_Effect': '结构效应（全球）',
                                    'Rate_Effect': '费率效应（全球）',
                                    'Total_Contribution': '对全球单车边际贡献'
                                }).style.format({
                                    '基期销量': '{:,.0f}',
                                    '基期占比%': '{:.1f}%',
                                    '当期销量': '{:,.0f}',
                                    '当期占比%': '{:.1f}%',
                                    '基期单车边际': '¥{:,.0f}',
                                    '当期单车边际': '¥{:,.0f}',
                                    '结构效应（全球）': '{:+,.0f}',
                                    '费率效应（全球）': '{:+,.0f}',
                                    '对全球单车边际贡献': '{:+,.0f}'
                                }),
                                use_container_width=True
                            )
        
        st.markdown("---")

else:
    # 未加载数据时显示说明
    st.info("👈 请在左侧边栏上传数据文件")
    
    with st.expander("📖 使用说明", expanded=True):
        st.markdown("""
        ### 数据格式要求
        
        | 列名 | Month | Dim_A | Dim_B | Dim_C | Dim_D | Dim_E | Sales Volume | Total Margin |
        |------|-------|-------|-------|-------|-------|-------|--------------|--------------|
        | 说明 | 月份 | 维度A | 维度B | 维度C | 维度D | 维度E | 销量 | 边际总额 |
        | 默认 | - | 大区 | 国家 | 车型 | 燃油品类 | 品牌 | - | - |
        
        > 💡 **提示**：
        > - Dim_D 和 Dim_E 为可选列，如果数据中不包含则不会显示
        > - 上传数据后可在侧边栏"自定义维度名称"中修改各维度的显示名称
        
        ### 计算逻辑 (自底向上)
        
        1. **原子化计算**: 首先在最细颗粒度（所有维度的组合）上计算每个细分项的 PVM 效应。
        2. **结构效应 (Mix)**: 细分项权重变化带来的影响。
        3. **费率效应 (Rate)**: 细分项单车边际变化带来的影响。
        4. **维度聚合**: 将细分项的效应汇总到当前查看的维度（如大区）。
        
        > 💡 这种方法能确保大区内部的产品结构变化正确归因为结构效应，而不是费率效应。
        """)

# ==================== 页脚 ====================
st.markdown("---")

# 添加PVM效应计算假设说明
with st.expander("📐 PVM效应计算假设说明", expanded=False):
    st.markdown("""
    <style>
        .assumption-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
            margin: 1rem 0;
            font-family: 'Lora', Georgia, serif;
        }
        .assumption-table th {
            background: linear-gradient(135deg, rgba(217, 119, 87, 0.15), rgba(106, 155, 204, 0.1));
            color: #141413;
            padding: 12px 15px;
            text-align: center;
            border: 1px solid #e8e6dc;
            font-weight: 600;
            font-family: 'Poppins', Arial, sans-serif;
        }
        .assumption-table td {
            padding: 10px 15px;
            border: 1px solid #e8e6dc;
            color: #141413;
        }
        .assumption-table tr:nth-child(even) {
            background: rgba(250, 249, 245, 0.8);
        }
        .assumption-table tr:hover {
            background: rgba(217, 119, 87, 0.08);
        }
        .product-type {
            font-weight: 600;
            color: #d97757;
        }
        .formula {
            font-family: 'Consolas', monospace;
            color: #b0aea5;
        }
    </style>
    
    <table class="assumption-table">
        <tr>
            <th style="width: 15%;">产品类型</th>
            <th style="width: 50%;">结构效应 (Mix Effect)</th>
            <th style="width: 35%;">费率效应 (Rate Effect)</th>
        </tr>
        <tr>
            <td class="product-type">现有产品</td>
            <td class="formula">(当期权重 - 基期权重) × (基期单车边际 - 基期平均单车边际)</td>
            <td class="formula">当期权重 × (当期单车边际 - 基期单车边际)</td>
        </tr>
        <tr>
            <td class="product-type">0→N产品</td>
            <td class="formula">当期权重 × (当期单车边际 - 基期平均单车边际)</td>
            <td style="text-align: center; color: #b0aea5;">0</td>
        </tr>
        <tr>
            <td class="product-type">N→0产品</td>
            <td class="formula">- 基期权重 × (基期单车边际 - 基期平均单车边际)</td>
            <td style="text-align: center; color: #b0aea5;">0</td>
        </tr>
    </table>
    
    <p style="color: #b0aea5; font-size: 0.85rem; margin-top: 1rem;">
        💡 <b>说明：</b>所有计算均在最细颗粒度进行，展示的数值为细分项汇总结果。这样可以避免高层级维度掩盖实际的结构变化。
    </p>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <div style='text-align: center; padding: 2rem 0;'>
        <span style='
            background: linear-gradient(90deg, #d97757, #6a9bcc, #788c5d); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent;
            font-weight: 600;
            font-size: 1.1rem;
            letter-spacing: 0.1em;
            font-family: Poppins, Arial, sans-serif;
        '>
            ✧ 财务分析驾驶舱 ✧
        </span>
        <br/>
        <span style='color: #b0aea5; font-size: 0.75rem; letter-spacing: 0.15em; font-family: Poppins, Arial, sans-serif;'>
            PVM MARGIN ANALYSIS | POWERED BY STREAMLIT & PLOTLY
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

