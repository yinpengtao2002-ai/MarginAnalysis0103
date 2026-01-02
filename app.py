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

# ==================== 投行风格CSS ====================
st.markdown("""
<style>
    /* 导入Google字体 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700;900&display=swap');
    
    /* 全局背景 - 深色投行风格 */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
    }
    
    /* 主标题容器 */
    .title-container {
        text-align: center;
        padding: 2.5rem 0 1.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    /* 装饰线条 - 动态扫光效果 */
    .title-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 400px;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #f5af19 20%, #ffd700 50%, #f5af19 80%, transparent 100%);
        animation: lineGlow 4s ease-in-out infinite;
    }
    
    .title-container::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 500px;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.5), transparent);
        animation: lineGlow 4s ease-in-out infinite reverse;
    }
    
    @keyframes lineGlow {
        0%, 100% { opacity: 0.3; width: 200px; }
        50% { opacity: 1; width: 500px; }
    }
    
    /* 主标题样式 - 极致精美 */
    .main-header {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffd700 0%, #ffcc00 20%, #ff9500 40%, #ffcc00 60%, #ffd700 80%, #ffe066 100%);
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 0.5rem 0;
        letter-spacing: 0.15em;
        font-family: 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
        animation: shimmer 4s ease-in-out infinite, float 6s ease-in-out infinite;
        position: relative;
        display: inline-block;
    }
    
    @keyframes shimmer {
        0% { background-position: 0% center; }
        50% { background-position: 100% center; }
        100% { background-position: 0% center; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    /* 标题光晕效果 - 更强烈 */
    .title-glow {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 700px;
        height: 150px;
        background: radial-gradient(ellipse, rgba(255, 200, 0, 0.25) 0%, rgba(255, 150, 0, 0.1) 40%, transparent 70%);
        pointer-events: none;
        z-index: -1;
        animation: pulse 3s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.6; transform: translate(-50%, -50%) scale(1); }
        50% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); }
    }
    
    /* 副标题 - 更精致 */
    .sub-header {
        text-align: center;
        background: linear-gradient(90deg, rgba(148, 163, 184, 0.6), rgba(255, 215, 0, 0.8), rgba(148, 163, 184, 0.6));
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1rem;
        margin-top: 0.8rem;
        margin-bottom: 2.5rem;
        letter-spacing: 0.5em;
        font-weight: 600;
        text-transform: uppercase;
        animation: shimmer 5s ease-in-out infinite;
    }
    
    /* 装饰图标 - 更炫酷 */
    .header-icon {
        font-size: 3rem;
        display: block;
        margin-bottom: 0.8rem;
        filter: drop-shadow(0 0 30px rgba(255, 215, 0, 0.8));
        animation: iconFloat 3s ease-in-out infinite, iconGlow 2s ease-in-out infinite;
    }
    
    @keyframes iconFloat {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        25% { transform: translateY(-8px) rotate(-5deg); }
        75% { transform: translateY(-8px) rotate(5deg); }
    }
    
    @keyframes iconGlow {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.6)); }
        50% { filter: drop-shadow(0 0 40px rgba(255, 215, 0, 1)); }
    }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(255, 215, 0, 0.15);
    }
    
    /* 确保侧边栏展开按钮可见 */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        color: #f5af19 !important;
    }
    
    button[kind="headerNoPadding"] {
        display: flex !important;
        visibility: visible !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #f5af19;
        font-weight: 600;
        letter-spacing: 0.1em;
        border-left: 3px solid #f5af19;
        padding-left: 0.8rem;
        margin-left: -0.5rem;
    }
    
    /* 指标卡片 - 高级玻璃态 */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.95) 0%, rgba(22, 33, 62, 0.95) 100%);
        border: 1px solid rgba(255, 215, 0, 0.25);
        border-radius: 20px;
        padding: 1.8rem;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.5), 
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            0 0 30px rgba(255, 215, 0, 0.05);
        backdrop-filter: blur(15px);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 
            0 15px 50px rgba(0, 0, 0, 0.6), 
            inset 0 1px 0 rgba(255, 255, 255, 0.15),
            0 0 40px rgba(255, 215, 0, 0.1);
        border-color: rgba(255, 215, 0, 0.4);
    }
    
    [data-testid="stMetric"] label {
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffd700 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        font-size: 0.95rem !important;
    }
    
    /* 图表容器 */
    .chart-section {
        background: linear-gradient(135deg, rgba(15, 15, 26, 0.95) 0%, rgba(26, 26, 46, 0.95) 100%);
        border: 1px solid rgba(255, 215, 0, 0.15);
        border-radius: 24px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.5);
    }
    
    /* 子标题样式增强 */
    h3 {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid transparent;
        border-image: linear-gradient(90deg, #f5af19, transparent) 1;
        margin-bottom: 1rem !important;
    }
    
    /* 信息提示框 */
    .stAlert {
        background: rgba(26, 26, 46, 0.9) !important;
        border: 1px solid rgba(255, 215, 0, 0.2) !important;
        border-radius: 14px !important;
        backdrop-filter: blur(10px);
    }
    
    /* 展开器 */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%) !important;
        border: 1px solid rgba(255, 215, 0, 0.15) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
    }
    
    /* 数据表格 */
    .stDataFrame {
        background: rgba(15, 15, 26, 0.95) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 215, 0, 0.1) !important;
    }
    
    /* 分割线 */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.3), transparent) !important;
        margin: 2rem 0 !important;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #f5af19 0%, #f12711 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        letter-spacing: 0.08em;
        padding: 0.6rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(245, 175, 25, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(245, 175, 25, 0.5);
    }
    
    /* 下拉框 */
    .stSelectbox > div > div {
        background: rgba(26, 26, 46, 0.95) !important;
        border: 1px solid rgba(255, 215, 0, 0.2) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
    }
    
    /* Radio按钮 */
    .stRadio > div {
        background: rgba(26, 26, 46, 0.6);
        border-radius: 12px;
        padding: 0.8rem;
        border: 1px solid rgba(255, 215, 0, 0.1);
    }
    
    /* 成功提示 */
    .stSuccess {
        background: rgba(16, 185, 129, 0.15) !important;
        border: 1px solid rgba(16, 185, 129, 0.4) !important;
    }
    
    /* 文件上传器 */
    .stFileUploader {
        background: rgba(26, 26, 46, 0.6);
        border: 2px dashed rgba(255, 215, 0, 0.25);
        border-radius: 16px;
        padding: 1.2rem;
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
        background: rgba(26, 26, 46, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #f5af19, #f12711);
        border-radius: 4px;
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


def calculate_pvm_effects(curr_df, base_df, dimension_col, 
                          global_vol_curr, global_vol_base, global_avg_margin_base):
    """
    计算PVM效应
    
    特殊处理：
    - 新品（基期销量为0）：费率效应为0，
      结构效应 = Weight_Curr × (Margin_Curr - Global_Avg_Base)
    - 停产品（当期销量为0）：费率效应为0，
      结构效应 = (0 - Weight_Base) × (Margin_Base - Global_Avg_Base)
    """
    # 合并当期和基期数据
    merged = pd.merge(
        curr_df[[dimension_col, 'Sales Volume', 'Unit Margin']].rename(
            columns={'Sales Volume': 'Vol_Curr', 'Unit Margin': 'Margin_Unit_Curr'}
        ),
        base_df[[dimension_col, 'Sales Volume', 'Unit Margin']].rename(
            columns={'Sales Volume': 'Vol_Base', 'Unit Margin': 'Margin_Unit_Base'}
        ),
        on=dimension_col,
        how='outer'
    ).fillna(0)
    
    # 计算权重
    merged['Weight_Curr'] = merged['Vol_Curr'] / global_vol_curr if global_vol_curr > 0 else 0
    merged['Weight_Base'] = merged['Vol_Base'] / global_vol_base if global_vol_base > 0 else 0
    
    # 识别新品（基期销量为0，当期销量>0）和停产品（当期销量为0，基期销量>0）
    is_new_product = (merged['Vol_Base'] == 0) & (merged['Vol_Curr'] > 0)
    is_discontinued = (merged['Vol_Curr'] == 0) & (merged['Vol_Base'] > 0)
    is_existing = ~is_new_product & ~is_discontinued
    
    # 创建用于计算的虚拟边际列
    # 对新品：虚拟基期边际 = 当期边际（使结构效应用当期边际计算）
    # 对停产品和现有产品：虚拟基期边际 = 实际基期边际
    merged['Effective_Margin_Base'] = merged['Margin_Unit_Base'].copy()
    merged.loc[is_new_product, 'Effective_Margin_Base'] = merged.loc[is_new_product, 'Margin_Unit_Curr']
    
    # 初始化效应列
    merged['Relative_Mix_Effect'] = 0.0
    merged['Rate_Effect'] = 0.0
    
    # === 现有产品：正常计算 ===
    # 结构效应 = (Weight_Curr - Weight_Base) × (Margin_Unit_Base - Global_Avg_Base)
    # 费率效应 = Weight_Curr × (Margin_Unit_Curr - Margin_Unit_Base)
    merged.loc[is_existing, 'Relative_Mix_Effect'] = \
        (merged.loc[is_existing, 'Weight_Curr'] - merged.loc[is_existing, 'Weight_Base']) * \
        (merged.loc[is_existing, 'Margin_Unit_Base'] - global_avg_margin_base)
    merged.loc[is_existing, 'Rate_Effect'] = \
        merged.loc[is_existing, 'Weight_Curr'] * \
        (merged.loc[is_existing, 'Margin_Unit_Curr'] - merged.loc[is_existing, 'Margin_Unit_Base'])
    
    # === 新品：费率效应=0，结构效应用当期边际 ===
    # 结构效应 = Weight_Curr × (Margin_Curr - Global_Avg_Base)
    # 费率效应 = 0（新品没有历史价格波动）
    merged.loc[is_new_product, 'Relative_Mix_Effect'] = \
        merged.loc[is_new_product, 'Weight_Curr'] * \
        (merged.loc[is_new_product, 'Margin_Unit_Curr'] - global_avg_margin_base)
    merged.loc[is_new_product, 'Rate_Effect'] = 0
    
    # === 停产品：费率效应=0，结构效应用基期边际 ===
    # 结构效应 = (0 - Weight_Base) × (Margin_Base - Global_Avg_Base)
    # 费率效应 = 0（当期权重为0）
    merged.loc[is_discontinued, 'Relative_Mix_Effect'] = \
        (0 - merged.loc[is_discontinued, 'Weight_Base']) * \
        (merged.loc[is_discontinued, 'Margin_Unit_Base'] - global_avg_margin_base)
    merged.loc[is_discontinued, 'Rate_Effect'] = 0
    
    # 更新显示用的边际
    # 新品的基期边际显示为全球基期平均边际（因为新品没有历史数据，用基期总体平均作为参考）
    merged.loc[is_new_product, 'Margin_Unit_Base'] = global_avg_margin_base
    # 停产品的当期边际显示为全球基期平均边际（因为停产品当期没有数据）
    merged.loc[is_discontinued, 'Margin_Unit_Curr'] = global_avg_margin_base
    
    # 总贡献
    merged['Total_Contribution'] = merged['Relative_Mix_Effect'] + merged['Rate_Effect']
    
    return merged


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
    
    # 投行风格颜色方案
    color_schemes = {
        'gold': {
            'increasing': '#10b981',
            'decreasing': '#ef4444',
            'total': '#ffd700',
            'base': '#3b82f6'
        },
        'emerald': {
            'increasing': '#34d399',
            'decreasing': '#f87171',
            'total': '#fbbf24',
            'base': '#60a5fa'
        },
        'royal': {
            'increasing': '#22d3d3',
            'decreasing': '#fb7185',
            'total': '#a78bfa',
            'base': '#38bdf8'
        }
    }
    colors = color_schemes.get(color_scheme, color_schemes['gold'])
    
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
        textfont=dict(size=13, color='#e2e8f0', family='Microsoft YaHei'),
        increasing={"marker": {"color": colors['increasing'], "line": {"color": colors['increasing'], "width": 1}}},
        decreasing={"marker": {"color": colors['decreasing'], "line": {"color": colors['decreasing'], "width": 1}}},
        totals={"marker": {"color": colors['total'], "line": {"color": colors['total'], "width": 2}}},
        connector={"line": {"color": "rgba(255, 215, 0, 0.2)", "width": 1.5, "dash": "dot"}},
    ))
    
    fig.update_layout(
        title={
            'text': f'<b>{title}</b>',
            'font': {'size': 18, 'color': '#ffd700', 'family': 'Microsoft YaHei'},
            'x': 0.5,
            'xanchor': 'center'
        },
        showlegend=False,
        height=520,
        margin=dict(l=80, r=80, t=120, b=100),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            tickangle=-25,
            tickfont=dict(size=12, color='#94a3b8', family='Microsoft YaHei'),
            gridcolor='rgba(255, 215, 0, 0.05)',
            linecolor='rgba(255, 215, 0, 0.2)',
            showline=True
        ),
        yaxis=dict(
            title=dict(text='单车边际 (¥)', font=dict(size=13, color='#94a3b8')),
            gridcolor='rgba(255, 215, 0, 0.08)',
            tickfont=dict(size=11, color='#94a3b8'),
            tickformat=',.0f',
            linecolor='rgba(255, 215, 0, 0.2)',
            showline=True,
            range=[y_range_min, y_range_max],  # 灵活的Y轴范围
            zeroline=False
        ),
        hoverlabel=dict(
            bgcolor='rgba(26, 26, 46, 0.98)',
            bordercolor='rgba(255, 215, 0, 0.5)',
            font=dict(size=13, color='#e2e8f0', family='Microsoft YaHei')
        )
    )
    
    # 添加注释 - 变动金额
    delta_val = curr_margin - base_margin
    pct_change = (delta_val / base_margin * 100) if base_margin != 0 else 0
    delta_color = '#10b981' if delta_val >= 0 else '#ef4444'
    
    fig.add_annotation(
        x=0.5,
        y=1.08,
        xref='paper',
        yref='paper',
        text=f'<b>变动: ¥{delta_val:+,.0f}</b>  <span style="color: {delta_color}">({pct_change:+.2f}%)</span>',
        showarrow=False,
        font=dict(size=15, color=delta_color, family='Microsoft YaHei'),
        bgcolor='rgba(26, 26, 46, 0.9)',
        bordercolor='rgba(255, 215, 0, 0.3)',
        borderwidth=1,
        borderpad=10
    )
    
    return fig


# ==================== 主界面 ====================
st.markdown("""
<div class="title-container">
    <div class="title-glow"></div>
    <span class="header-icon">🚀</span>
    <h1 class="main-header">单车边际变动归因分析</h1>
</div>
<p class="sub-header">◆ UNIT MARGIN ATTRIBUTION ANALYSIS ◆</p>
""", unsafe_allow_html=True)

# ==================== 侧边栏 ====================
with st.sidebar:
    # 维度配置
    if st.session_state.data_loaded:
        # 数据已加载，使用折叠的expander
        with st.expander("⚙️ 维度配置", expanded=False):
            st.caption("设置各维度的显示名称（修改后自动更新）")
            for dim in ALL_DIMENSIONS:
                new_value = st.text_input(
                    f"{dim}",
                    value=st.session_state.custom_dim_names.get(dim, dim),
                    key=f"dim_name_{dim}_loaded"
                )
                # 如果值改变了，直接更新session_state
                if new_value != st.session_state.custom_dim_names.get(dim):
                    st.session_state.custom_dim_names[dim] = new_value
                    st.rerun()
    else:
        # 数据未加载，直接显示配置
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
        st.markdown("---")
    
    # 数据中心
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
                # 首次加载成功，触发rerun来折叠配置区域
                st.session_state.data_loaded = True
                st.rerun()
        else:
            df = None
    
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
    color_schemes = ['gold', 'emerald', 'royal']
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
        
        # 聚合数据
        base_data = aggregate_data(df_level, [dim], base_month)
        curr_data = aggregate_data(df_level, [dim], curr_month)
        
        if not base_data.empty and not curr_data.empty:
            # 计算筛选范围内的指标
            level_vol_base = base_data['Sales Volume'].sum()
            level_vol_curr = curr_data['Sales Volume'].sum()
            level_margin_base = base_data['Total Margin'].sum() if 'Total Margin' in base_data.columns else (base_data['Sales Volume'] * base_data['Unit Margin']).sum()
            level_margin_curr = curr_data['Total Margin'].sum() if 'Total Margin' in curr_data.columns else (curr_data['Sales Volume'] * curr_data['Unit Margin']).sum()
            level_avg_margin_base = level_margin_base / level_vol_base if level_vol_base > 0 else 0
            level_avg_margin_curr = level_margin_curr / level_vol_curr if level_vol_curr > 0 else 0
            
            # 计算PVM效应（使用筛选范围内的指标）
            effects = calculate_pvm_effects(
                curr_data, base_data, dim,
                level_vol_curr if is_drilled else global_vol_curr,
                level_vol_base if is_drilled else global_vol_base,
                level_avg_margin_base if is_drilled else global_avg_margin_base
            )
            
            # 创建瀑布图
            fig = create_waterfall_chart(
                effects, dim,
                f'{dim_name}贡献分解 ({base_month} → {curr_month})',
                level_avg_margin_base if is_drilled else global_avg_margin_base,
                level_avg_margin_curr if is_drilled else global_avg_margin_curr,
                color_schemes[level % len(color_schemes)]
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # 显示明细数据
            with st.expander(f"📋 {dim_name}明细数据"):
                display_df = prepare_display_dataframe(
                    effects, dim,
                    level_vol_base if is_drilled else global_vol_base,
                    level_vol_curr if is_drilled else global_vol_curr,
                    level_margin_base if is_drilled else global_margin_base,
                    level_margin_curr if is_drilled else global_margin_curr
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
                
                # 如果是下钻状态，额外显示对全球整体单车边际的贡献
                if is_drilled:
                    st.markdown("---")
                    st.markdown("##### 🌐 对全球整体单车边际的贡献")
                    
                    # 基于全球销量重新计算PVM效应
                    global_effects = calculate_pvm_effects(
                        curr_data, base_data, dim,
                        global_vol_curr, global_vol_base, global_avg_margin_base
                    )
                    
                    global_display_df = prepare_display_dataframe(
                        global_effects, dim,
                        global_vol_base, global_vol_curr,
                        global_margin_base, global_margin_curr,
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
        
        ### 计算公式
        
        - **权重**: Weight = Volume / Global_Volume
        - **结构效应**: (Weight_Curr - Weight_Base) × (Margin_Base - Global_Avg_Margin_Base)
        - **费率效应**: Weight_Curr × (Margin_Curr - Margin_Base)
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
        }
        .assumption-table th {
            background: linear-gradient(135deg, rgba(245, 175, 25, 0.3), rgba(255, 215, 0, 0.2));
            color: #ffd700;
            padding: 12px 15px;
            text-align: center;
            border: 1px solid rgba(255, 215, 0, 0.3);
            font-weight: 600;
        }
        .assumption-table td {
            padding: 10px 15px;
            border: 1px solid rgba(255, 215, 0, 0.15);
            color: #e2e8f0;
        }
        .assumption-table tr:nth-child(even) {
            background: rgba(26, 26, 46, 0.5);
        }
        .assumption-table tr:hover {
            background: rgba(255, 215, 0, 0.05);
        }
        .product-type {
            font-weight: 600;
            color: #ffd700;
        }
        .formula {
            font-family: 'Consolas', monospace;
            color: #94a3b8;
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
            <td style="text-align: center; color: #94a3b8;">0</td>
        </tr>
        <tr>
            <td class="product-type">N→0产品</td>
            <td class="formula">- 基期权重 × (基期单车边际 - 基期平均单车边际)</td>
            <td style="text-align: center; color: #94a3b8;">0</td>
        </tr>
    </table>
    
    <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 1rem;">
        💡 <b>说明：</b>0→N产品没有历史价格波动，全部影响归于结构效应（反映其是否比基期平均水平更赚钱），费率效应为0；
    </p>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <div style='text-align: center; padding: 2rem 0;'>
        <span style='
            background: linear-gradient(90deg, #ffd700, #ff8c00, #ffd700); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent;
            background-size: 200% auto;
            font-weight: 700;
            font-size: 1.1rem;
            letter-spacing: 0.15em;
        '>
            ✧ 财务分析驾驶舱 ✧
        </span>
        <br/>
        <span style='color: rgba(148, 163, 184, 0.5); font-size: 0.75rem; letter-spacing: 0.2em;'>
            PVM MARGIN ANALYSIS | POWERED BY STREAMLIT & PLOTLY
        </span>
    </div>
    """,
    unsafe_allow_html=True
)
