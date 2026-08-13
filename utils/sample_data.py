# utils/sample_data.py
import pandas as pd
import numpy as np
import datetime

# Seed for reproducibility
np.random.seed(42)

def generate_projects_data():
    project_names = [
        "Apex Tower Phase 1", "Riverfront Condos", "Metro Highway Expansion", "Centennial Transit Hub",
        "Vanguard Logistics Center", "Summit Ridge Hospital", "Innovation Tech Park", "Lakeside Water Plant",
        "Grand Library Renovation", "Emerald Eco-Village", "Titan Industrial Complex", "Aura Luxury Suites",
        "Pinnacle Office Plaza", "Solar Field Facility", "Bridge Repair - Sector 4", "Marina Bay Boardwalk",
        "Eastside Community School", "Horizon Data Center", "Crossroads Mall Upgrade", "Northwest Wind Farm"
    ]
    
    clients = [
        "Apex Development Corp", "Riverfront LLC", "State Dept of Transportation", "Metropolitan Transit Authority",
        "Vanguard Logistics Ltd", "Summit Health Group", "Innovation Real Estate", "Municipal Water Board",
        "City Library Foundation", "Eco-Living Group", "Titan Heavy Industries", "Aura Developments",
        "Pinnacle Group LLC", "CleanEnergy Inc", "County Highway Commission", "Port Authority",
        "School District 12", "Horizon Cloud Services", "Retail Properties Inc", "Northwest Power Corp"
    ]
    
    locations = [
        "Hyderabad","Visakhapatnam","Bengaluru","Chennai","Mumbai","Delhi","Pune","Kolkata",
        "Ahmedabad","Kochi", "Lucknow", "Jaipur", "Bhubaneswar", "Nagpur", "Indore", "Vijayawada", "Warangal",
        "Coimbatore","Surat","Mysuru"
    ]
    
    engineers = [
        "Dr. Sarah Jenkins", "David Miller, PE", "Elena Rostova", "Marcus Vance",
        "Robert Chen", "Sophia Al-Jamil", "Thomas Wright", "Patricia Gomez",
        "James O'Connor", "Yuki Tanaka", "Kevin Peterson", "Amanda Ross",
        "Zack Taylor", "Rachel Green", "Omar Farooq", "Emily Watson",
        "Brian Kelly", "Nina Patel", "Charles Dupont", "Laura Vance"
    ]
    
    status_options = ["Active", "Completed", "Delayed", "Planning"]
    
    data = []
    base_date = datetime.date(2025, 1, 1)
    
    for i in range(20):
        # Determine budget and status
        budget = int(np.random.randint(15, 150) * 100000)
        status = np.random.choice(status_options, p=[0.5, 0.25, 0.15, 0.1])
        
        # Determine completion percentage and spend based on status
        if status == "Completed":
            completion = 100
            spend = int(budget * np.random.uniform(0.95, 1.05))
        elif status == "Planning":
            completion = 0
            spend = 0
        elif status == "Delayed":
            completion = int(np.random.randint(30, 85))
            spend = int(budget * (completion / 100) * np.random.uniform(1.1, 1.25)) # cost overrun
        else: # Active
            completion = int(np.random.randint(10, 95))
            spend = int(budget * (completion / 100) * np.random.uniform(0.95, 1.05))
            
        start_offset = np.random.randint(-300, 100)
        duration = np.random.randint(180, 540)
        start_date = base_date + datetime.timedelta(days=start_offset)
        end_date = start_date + datetime.timedelta(days=duration)
        
        # Risk level and AI metrics
        if status == "Delayed":
            risk = "High"
            health = np.random.randint(40, 65)
        elif status == "Active" and spend > budget * (completion / 100):
            risk = "Medium"
            health = np.random.randint(65, 80)
        elif status == "Planning":
            risk = "Low"
            health = np.random.randint(85, 95)
        else:
            risk = "Low"
            health = np.random.randint(80, 98)
            
        data.append({
            "Project ID": f"PRJ-{100+i:03d}",
            "Project Name": project_names[i],
            "Client": clients[i],
            "Location": locations[i],
            "Lead Engineer": engineers[i],
            "Start Date": start_date,
            "End Date": end_date,
            "Budget": budget,
            "Spend": spend,
            "Progress": completion,
            "Status": status,
            "Health Score": health,
            "Risk Level": risk
        })
        
    return pd.DataFrame(data)

def generate_employees_data(projects_df):
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth",
                   "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen",
                   "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra"]
    
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                  "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
                  "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"]
    
    roles = ["Engineer", "Supervisor", "Laborer", "Safety Officer", "Admin Officer"]
    role_weights = [0.15, 0.15, 0.60, 0.05, 0.05]
    
    data = []
    project_list = list(projects_df[projects_df["Status"] != "Planning"]["Project Name"])
    project_list.append("Unassigned")
    
    for i in range(100):
        fn = np.random.choice(first_names)
        ln = np.random.choice(last_names)
        name = f"{fn} {ln}"
        
        role = np.random.choice(roles, p=role_weights)
        
        if role in ["Engineer", "Supervisor", "Safety Officer"]:
            proj = np.random.choice(project_list)
        else: # Laborers/Admin
            proj = np.random.choice(project_list, p=[1.0/len(project_list)]*len(project_list))
            
        attendance = round(np.random.uniform(85, 100), 2)
        prod = round(np.random.uniform(60, 98), 1)
        
        if role == "Engineer":
            hourly = np.random.choice([65, 70, 75, 80, 85])
        elif role == "Supervisor":
            hourly = np.random.choice([40, 45, 50])
        elif role == "Laborer":
            hourly = np.random.choice([20, 22, 25, 28])
        else: # Safety/Admin
            hourly = np.random.choice([30, 35, 38])
            
        data.append({
            "Employee ID": f"EMP-{200+i:03d}",
            "Name": name,
            "Role": role,
            "Assigned Project": proj,
            "Hourly Rate ($)": hourly,
            "Attendance Rate (%)": attendance,
            "Productivity Index (%)": prod,
            "Status": np.random.choice(["Active", "On Leave", "Suspended"], p=[0.92, 0.06, 0.02]),
            "Contact": f"{fn.lower()}.{ln.lower()}@cihub-enterprise.com"
        })
        
    return pd.DataFrame(data)

def generate_materials_data():
    categories = {
        "Cement": ["Portland Cement Type I", "Portland Cement Type V", "Masonry Cement", "Rapid Hardening Cement"],
        "Steel": ["Rebar Grade 60 (10mm)", "Rebar Grade 60 (16mm)", "Structural Steel I-Beams", "Steel Mesh Reinforcement"],
        "Sand": ["Concrete Sand (Coarse)", "Masonry Sand (Fine)", "Fill Sand", "Silica Sand"],
        "Bricks": ["Standard Red Clay Bricks", "Concrete Blocks 8x8x16", "Fly Ash Bricks", "Fireclay Bricks"],
        "Aggregates": ["Coarse Gravel (20mm)", "Crushed Stone (10mm)", "Base Aggregate Road Gravel", "River Pebbles"],
        "Paint & Coatings": ["Exterior Acrylic Primer", "Exterior Weather-Shield Paint", "Anti-Rust Metal Primer", "Concrete Sealer"],
        "Electrical": ["PVC Conduit 2-inch", "Copper Wire 12/2 AWG", "Main Breaker Panel 200A", "Industrial LED Fixtures"],
        "Plumbing & HVAC": ["PVC Drain Pipes 4-inch", "Copper Tube 3/4-inch", "Industrial Valve 2-inch", "Flexible Ducting"],
        "Safety Gear": ["Hard Hats Class E", "Reflective Safety Vests", "Steel Toe Safety Boots", "Safety Harnesses Kit"]
    }
    
    suppliers = ["Matrix Materials Inc.", "Vulcan Building Solutions", "Pioneer Aggregates Co.", 
                 "Titan Steel Works", "Apex Build & Logistics", "Coastal Pipe & Fitting", 
                 "Giga Electrical Wholesalers", "Sherwin Coating Solutions"]
    
    units = {
        "Cement": "Bags (50kg)",
        "Steel": "Tons",
        "Sand": "Cubic Yards",
        "Bricks": "Units (1000s)",
        "Aggregates": "Tons",
        "Paint & Coatings": "Gallons",
        "Electrical": "Meters",
        "Plumbing & HVAC": "Units",
        "Safety Gear": "Units"
    }
    
    prices = {
        "Cement": [10.5, 12.0, 11.0, 14.5],
        "Steel": [850.0, 920.0, 1150.0, 600.0],
        "Sand": [35.0, 38.0, 22.0, 45.0],
        "Bricks": [320.0, 850.0, 280.0, 550.0],
        "Aggregates": [28.0, 32.0, 24.0, 42.0],
        "Paint & Coatings": [45.0, 65.0, 52.0, 80.0],
        "Electrical": [4.5, 8.2, 120.0, 35.0],
        "Plumbing & HVAC": [18.5, 32.0, 75.0, 22.5],
        "Safety Gear": [15.0, 8.5, 45.0, 65.0]
    }
    
    data = []
    
    counter = 0
    for cat, items in categories.items():
        for idx, item in enumerate(items):
            min_stock = np.random.randint(50, 500)
            # Give a few items low stock intentionally for dashboard notifications
            if counter in [2, 5, 12, 22, 38]:
                stock = np.random.randint(5, int(min_stock * 0.8))
            else:
                stock = np.random.randint(min_stock + 10, min_stock * 5)
                
            unit_price = prices[cat][idx]
            
            status = "In Stock"
            if stock == 0:
                status = "Out of Stock"
            elif stock < min_stock:
                status = "Low Stock"
                
            data.append({
                "Material ID": f"MAT-{300+counter:03d}",
                "Material Name": item,
                "Category": cat,
                "Stock Quantity": stock,
                "Minimum Stock": min_stock,
                "Unit": units[cat],
                "Unit Price ($)": unit_price,
                "Total Value ($)": round(stock * unit_price, 2),
                "Supplier": np.random.choice(suppliers),
                "Status": status
            })
            counter += 1
            
            # Cap at exactly 50 material records
            if counter >= 50:
                break
        if counter >= 50:
            break
            
    return pd.DataFrame(data)

def generate_budget_12months():
    months = ["Jul-25", "Aug-25", "Sep-25", "Oct-25", "Nov-25", "Dec-25", 
              "Jan-26", "Feb-26", "Mar-26", "Apr-26", "May-26", "Jun-26"]
    
    # Base pattern with realistic incremental changes
    planned = [4.2, 4.5, 4.8, 5.0, 5.2, 4.9, 4.1, 4.4, 4.9, 5.4, 5.8, 6.2] # Millions
    actual = []
    
    for i, p in enumerate(planned):
        # Simulate slight overrun trends in active months
        if i in [2, 3, 9, 10]:
            actual.append(round(p * np.random.uniform(1.05, 1.15), 2))
        else:
            actual.append(round(p * np.random.uniform(0.96, 1.03), 2))
            
    data = {
        "Month": months,
        "Planned Budget ($M)": planned,
        "Actual Spend ($M)": actual,
        "Labor Costs ($M)": [round(a * 0.35, 2) for a in actual],
        "Material Costs ($M)": [round(a * 0.42, 2) for a in actual],
        "Equipment Costs ($M)": [round(a * 0.15, 2) for a in actual],
        "Permits & Admin ($M)": [round(a * 0.08, 2) for a in actual]
    }
    
    return pd.DataFrame(data)

def generate_safety_data(projects_df):
    # Safety inspections and incidents mock data
    active_projects = projects_df[projects_df["Status"] != "Planning"]["Project Name"].tolist()
    
    data = []
    for i, proj in enumerate(active_projects):
        inspections = np.random.randint(15, 60)
        score = np.random.randint(80, 100)
        
        # Indecents distribution
        if score < 85:
            incidents = np.random.randint(1, 4)
            unresolved = np.random.randint(1, 3)
        elif score < 92:
            incidents = np.random.randint(0, 2)
            unresolved = np.random.randint(0, 2)
        else:
            incidents = 0
            unresolved = 0
            
        compliance = round(score * np.random.uniform(0.98, 1.0), 1)
        compliance = min(compliance, 100.0)
        
        # Risk factor
        if incidents > 0 or score < 85:
            risk = "Medium"
        elif score < 90:
            risk = "Medium"
        else:
            risk = "Low"
            
        data.append({
            "Project Name": proj,
            "Total Safety Inspections": inspections,
            "Safety Score (HSE)": score,
            "Minor Incidents": incidents,
            "Major Incidents": 0,
            "Unresolved Hazards": unresolved,
            "Compliance Index (%)": compliance,
            "Risk Rating": risk,
            "Last Audit Date": datetime.date(2026, 6, np.random.randint(1, 28))
        })
        
    return pd.DataFrame(data)

def generate_recent_activities():
    activities = [
        {"Timestamp": "2026-07-03 08:45 AM", "Category": "Safety", "Project": "Apex Tower Phase 1", "Activity": "Safety audit successfully completed. Overall Score: 96/100.", "Status": "Completed"},
        {"Timestamp": "2026-07-03 07:30 AM", "Category": "Material", "Project": "Riverfront Condos", "Activity": "Delivery of 250 bags of Portland Cement received from Matrix Materials Inc.", "Status": "Completed"},
        {"Timestamp": "2026-07-02 04:15 PM", "Category": "AI Alert", "Project": "Metro Highway Expansion", "Activity": "AI predicted a 12-day weather delay for road paving activities next week.", "Status": "Attention"},
        {"Timestamp": "2026-07-02 11:00 AM", "Category": "Finance", "Project": "Summit Ridge Hospital", "Activity": "Invoice #SRH-7821 for $142,500 approved by Project Manager.", "Status": "Completed"},
        {"Timestamp": "2026-07-01 03:30 PM", "Category": "Workforce", "Project": "Centennial Transit Hub", "Activity": "12 structural bricklayers reallocated to support delayed subway entrance works.", "Status": "Completed"},
        {"Timestamp": "2026-07-01 09:00 AM", "Category": "Material", "Project": "Solar Field Facility", "Activity": "Warning: Steel Mesh stock is below safety threshold (Currently 45/200 units).", "Status": "Warning"},
        {"Timestamp": "2026-06-30 02:00 PM", "Category": "Safety", "Project": "Bridge Repair - Sector 4", "Activity": "OSHA Inspector visited the site. Zero compliance violations noted.", "Status": "Completed"},
        {"Timestamp": "2026-06-30 10:15 AM", "Category": "Finance", "Project": "Aura Luxury Suites", "Activity": "Monthly cost performance report generated: 4% under planned budget.", "Status": "Completed"}
    ]
    return pd.DataFrame(activities)

def get_all_data():
    """Returns a consolidated dictionary of all dataframes, initializing if not present."""
    projects = generate_projects_data()
    employees = generate_employees_data(projects)
    materials = generate_materials_data()
    budget = generate_budget_12months()
    safety = generate_safety_data(projects)
    activities = generate_recent_activities()
    
    return {
        "projects": projects,
        "employees": employees,
        "materials": materials,
        "budget": budget,
        "safety": safety,
        "activities": activities
    }
