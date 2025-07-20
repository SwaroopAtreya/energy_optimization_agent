import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import random

# Page configuration
st.set_page_config(
    page_title="AI Energy Optimizer",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
}
.savings-positive {
    color: #28a745;
    font-weight: bold;
}
.alert-warning {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Simulated data generation functions
@st.cache_data
def generate_resource_data():
    """Generate simulated resource usage data"""
    np.random.seed(42)
    hours = pd.date_range(start='2025-01-01', periods=168, freq='H')  # 7 days
    
    data = []
    for i, hour in enumerate(hours):
        # Simulate realistic workload patterns
        base_cpu = 45 + 20 * np.sin(2 * np.pi * i / 24)  # Daily pattern
        base_memory = 60 + 15 * np.sin(2 * np.pi * i / 24)
        base_gpu = max(0, 30 + 40 * np.sin(2 * np.pi * i / 24) + random.gauss(0, 10))
        
        # Add some inefficiencies
        cpu_waste = max(0, random.gauss(15, 5))
        memory_waste = max(0, random.gauss(10, 5))
        gpu_waste = max(0, random.gauss(20, 8))
        
        data.append({
            'timestamp': hour,
            'cpu_usage': min(95, base_cpu + random.gauss(0, 5)),
            'memory_usage': min(95, base_memory + random.gauss(0, 5)),
            'gpu_usage': min(95, base_gpu),
            'cpu_waste': cpu_waste,
            'memory_waste': memory_waste,
            'gpu_waste': gpu_waste,
            'energy_cost': (base_cpu + base_memory + base_gpu) * 0.12 + random.gauss(0, 2),
            'carbon_footprint': (base_cpu + base_memory + base_gpu) * 0.05 + random.gauss(0, 1)
        })
    
    return pd.DataFrame(data)

@st.cache_data
def get_optimization_suggestions():
    """Generate AI agent suggestions"""
    suggestions = [
        {
            'resource': 'GPU Cluster A',
            'issue': 'Idle 73% of the time',
            'action': 'Hibernate during off-peak hours',
            'potential_savings': '$450/month',
            'energy_reduction': '35% less power consumption',
            'confidence': 95,
            'risk_level': 'Low'
        },
        {
            'resource': 'CPU Pool B',
            'issue': 'Underutilized (avg 28%)',
            'action': 'Consolidate workloads',
            'potential_savings': '$280/month',
            'energy_reduction': '22% efficiency gain',
            'confidence': 88,
            'risk_level': 'Medium'
        },
        {
            'resource': 'Memory Cache C',
            'issue': 'Over-provisioned by 40%',
            'action': 'Right-size allocation',
            'potential_savings': '$320/month',
            'energy_reduction': '18% memory optimization',
            'confidence': 92,
            'risk_level': 'Low'
        }
    ]
    return suggestions

def ai_agent_simulation():
    """Simulate AI agent decision making"""
    decisions = [
        "🤖 Analyzing resource utilization patterns...",
        "📊 Detecting idle GPU resources (ID: gpu-cluster-a)",
        "⚡ Energy waste detected: 450kWh/month",
        "💡 Recommendation: Implement auto-hibernation schedule",
        "🔧 Calculating optimal scaling parameters...",
        "✅ Action approved: Scheduling hibernation for 22:00-06:00",
        "📈 Projected savings: $450/month, 35% energy reduction"
    ]
    return decisions

# Main app layout
def main():
    # Header
    st.markdown('<h1 class="main-header">🌱 AI Energy Optimizer Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Autonomous Infrastructure Optimization for Sustainable Computing</p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("🔧 Control Panel")
    
    # Simulation controls
    simulation_speed = st.sidebar.slider("Simulation Speed", 1, 10, 5)
    auto_optimize = st.sidebar.checkbox("Enable Auto-Optimization", value=True)
    
    st.sidebar.markdown("---")
    st.sidebar.header("📊 Current Status")
    
    # Load data
    df = generate_resource_data()
    suggestions = get_optimization_suggestions()
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_cost = df['energy_cost'].iloc[-24:].sum()  # Last 24 hours
        st.metric("💰 Daily Energy Cost", f"${current_cost:.2f}", delta=f"-${current_cost*0.15:.2f}")
    
    with col2:
        avg_cpu = df['cpu_usage'].iloc[-24:].mean()
        st.metric("🖥️ Avg CPU Usage", f"{avg_cpu:.1f}%", delta=f"{avg_cpu-45:.1f}%")
    
    with col3:
        total_waste = (df['cpu_waste'].iloc[-24:] + df['memory_waste'].iloc[-24:] + df['gpu_waste'].iloc[-24:]).sum()
        st.metric("⚠️ Resource Waste", f"{total_waste:.0f} units", delta=f"-{total_waste*0.3:.0f}")
    
    with col4:
        carbon_today = df['carbon_footprint'].iloc[-24:].sum()
        st.metric("🌍 Carbon Footprint", f"{carbon_today:.1f} kg CO2", delta=f"-{carbon_today*0.25:.1f} kg")
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Real-time Monitoring", "🤖 AI Agent Actions", "💡 Optimization Suggestions", "💰 ROI Calculator"])
    
    with tab1:
        st.subheader("Resource Utilization Over Time")
        
        # Resource usage charts
        col1, col2 = st.columns(2)
        
        with col1:
            # CPU and Memory usage
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['cpu_usage'], name='CPU Usage', line=dict(color='#1f77b4')))
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['memory_usage'], name='Memory Usage', line=dict(color='#ff7f0e')))
            fig.update_layout(title="CPU & Memory Utilization", yaxis_title="Usage (%)", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # GPU usage and waste
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['gpu_usage'], name='GPU Usage', line=dict(color='#2ca02c')))
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['gpu_waste'], name='GPU Waste', line=dict(color='#d62728'), fill='tozeroy'))
            fig.update_layout(title="GPU Utilization & Waste", yaxis_title="Usage (%)", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Energy cost trend
        fig = px.area(df.iloc[-72:], x='timestamp', y='energy_cost', title="Energy Cost Trend (Last 3 Days)")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🤖 AI Agent Live Decision Making")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Current Analysis")
            
            # Simulate real-time agent thinking
            if st.button("▶️ Start AI Agent Analysis", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                decisions = ai_agent_simulation()
                
                for i, decision in enumerate(decisions):
                    status_text.text(decision)
                    progress_bar.progress((i + 1) / len(decisions))
                    time.sleep(1 / simulation_speed)
                
                st.success("✅ Analysis complete! Optimization actions scheduled.")
                
                # Show decision summary
                st.markdown("### Decision Summary")
                st.info("""
                **Actions Taken:**
                - Scheduled GPU hibernation for off-peak hours (22:00-06:00)
                - Consolidated 3 underutilized CPU instances
                - Right-sized memory allocation for Cache Pool C
                
                **Expected Impact:**
                - Monthly savings: $1,050
                - Energy reduction: 28%
                - Carbon footprint reduction: 1.2 tons CO2/year
                """)
        
        with col2:
            st.markdown("### Agent Status")
            
            status_indicators = {
                "🟢 Monitoring": "Active",
                "🟡 Analysis": "Running",
                "🔵 Optimization": "Scheduled",
                "⚪ Learning": "Continuous"
            }
            
            for status, value in status_indicators.items():
                st.markdown(f"**{status}:** {value}")
            
            st.markdown("---")
            st.markdown("### Safety Checks")
            st.success("✅ All safety rules active")
            st.info("🛡️ Human approval required for critical changes")
            st.warning("⏱️ 5-minute rollback window enabled")
    
    with tab3:
        st.subheader("💡 Current Optimization Opportunities")
        
        for i, suggestion in enumerate(suggestions):
            with st.expander(f"🎯 Optimization #{i+1}: {suggestion['resource']}", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Issue:** {suggestion['issue']}")
                    st.markdown(f"**Recommended Action:** {suggestion['action']}")
                
                with col2:
                    st.markdown(f"**💰 Potential Savings:** {suggestion['potential_savings']}")
                    st.markdown(f"**⚡ Energy Impact:** {suggestion['energy_reduction']}")
                
                with col3:
                    st.markdown(f"**🎯 Confidence:** {suggestion['confidence']}%")
                    risk_color = "🟢" if suggestion['risk_level'] == 'Low' else "🟡" if suggestion['risk_level'] == 'Medium' else "🔴"
                    st.markdown(f"**{risk_color} Risk Level:** {suggestion['risk_level']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ Approve Action #{i+1}", key=f"approve_{i}"):
                        st.success(f"Action approved for {suggestion['resource']}!")
                
                with col2:
                    if st.button(f"❌ Reject #{i+1}", key=f"reject_{i}"):
                        st.info(f"Action rejected for {suggestion['resource']}")
    
    with tab4:
        st.subheader("💰 Return on Investment Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Current Infrastructure")
            
            num_servers = st.number_input("Number of Servers", value=50, min_value=1)
            avg_monthly_cost = st.number_input("Average Monthly Cost ($)", value=15000, min_value=100)
            current_efficiency = st.slider("Current Efficiency (%)", 30, 90, 65)
            
            # Calculate potential savings
            optimization_potential = (85 - current_efficiency) / 85 * 100  # Max 85% efficiency
            monthly_savings = avg_monthly_cost * (optimization_potential / 100) * 0.3  # 30% of waste can be optimized
            annual_savings = monthly_savings * 12
            
        with col2:
            st.markdown("### Projected with AI Optimization")
            
            st.metric("🎯 Target Efficiency", "80-85%", delta=f"+{85-current_efficiency}%")
            st.metric("💰 Monthly Savings", f"${monthly_savings:,.2f}", delta="New!")
            st.metric("📅 Annual Savings", f"${annual_savings:,.2f}", delta="Projected")
            
            # ROI calculation
            implementation_cost = 25000  # Estimated implementation cost
            roi_months = implementation_cost / monthly_savings if monthly_savings > 0 else 0
            
            st.metric("📈 ROI Timeline", f"{roi_months:.1f} months", delta="Break-even")
        
        # Savings visualization
        months = list(range(1, 13))
        cumulative_savings = [monthly_savings * i for i in months]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=months, y=cumulative_savings, name='Cumulative Savings', marker_color='lightgreen'))
        fig.add_hline(y=implementation_cost, line_dash="dash", line_color="red", 
                      annotation_text=f"Break-even: ${implementation_cost:,}")
        fig.update_layout(title="Cumulative Savings Over Time", xaxis_title="Months", yaxis_title="Savings ($)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Environmental impact
        st.markdown("### Environmental Impact")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            energy_saved = annual_savings * 0.8  # Rough energy cost correlation
            st.metric("⚡ Energy Saved", f"{energy_saved:,.0f} kWh/year")
        
        with col2:
            carbon_reduced = energy_saved * 0.4  # kg CO2 per kWh
            st.metric("🌍 Carbon Reduced", f"{carbon_reduced:,.0f} kg CO2/year")
        
        with col3:
            trees_equivalent = carbon_reduced / 21  # Average tree absorption per year
            st.metric("🌳 Trees Equivalent", f"{trees_equivalent:.0f} trees/year")

if __name__ == "__main__":
    main()