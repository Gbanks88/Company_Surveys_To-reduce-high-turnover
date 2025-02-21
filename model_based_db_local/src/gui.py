import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import httpx
from typing import Optional, Dict, Any
import json
from datetime import datetime
import uuid
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
import csv
import time

class ModelBasedRequirementsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Model-Based Requirements Management System")
        self.root.geometry("1400x900")
        
        # Style configuration
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 14, "bold"))
        style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))
        style.configure("Info.TLabel", font=("Helvetica", 10))
        
        # API client setup with retry
        self.setup_api_client()
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Create tabs
        self.models_tab = ttk.Frame(self.notebook)
        self.requirements_tab = ttk.Frame(self.notebook)
        self.uml_tab = ttk.Frame(self.notebook)
        self.matrix_tab = ttk.Frame(self.notebook)
        self.metadata_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.models_tab, text='System Models')
        self.notebook.add(self.requirements_tab, text='Requirements Management')
        self.notebook.add(self.uml_tab, text='UML Modeling')
        self.notebook.add(self.matrix_tab, text='Traceability Matrix')
        self.notebook.add(self.metadata_tab, text='Metadata & Analytics')
        
        # Initialize all tabs
        self.init_models_tab()
        self.init_requirements_tab()
        self.init_uml_tab()
        self.init_matrix_tab()
        self.init_metadata_tab()
        
        # Load initial data
        self.load_all_data()

    def setup_api_client(self):
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            try:
                self.client = httpx.Client(base_url="http://127.0.0.1:8001")
                # Test connection
                self.client.get("/")
                print("Successfully connected to API server")
                return
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    messagebox.showerror("Error", f"Failed to connect to API server: {str(e)}")
                    return
                print(f"Retrying connection... ({retry_count}/{max_retries})")
                time.sleep(1)

    def load_all_data(self):
        try:
            self.refresh_models()
            self.refresh_requirements()
            self.refresh_uml_diagrams()
            self.refresh_metadata()
            self.generate_matrix()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def refresh_models(self):
        try:
            response = self.client.get("/models/")
            if response.status_code == 200:
                models = response.json()
                self.model_listbox.delete(*self.model_listbox.get_children())
                for model in models:
                    self.model_listbox.insert('', 'end', values=(
                        model['name'],
                        model['type'],
                        model['status']
                    ))
                # Update model selection in UML tab
                self.diagram_model['values'] = [model['name'] for model in models]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh models: {str(e)}")

    def refresh_requirements(self):
        try:
            response = self.client.get("/requirements/")
            if response.status_code == 200:
                requirements = response.json()
                self.req_listbox.delete(*self.req_listbox.get_children())
                for req in requirements:
                    self.req_listbox.insert('', 'end', values=(
                        req['id'],
                        req['title'],
                        req['status'],
                        req['priority']
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh requirements: {str(e)}")

    def refresh_uml_diagrams(self):
        try:
            response = self.client.get("/uml/")
            if response.status_code == 200:
                diagrams = response.json()
                # Update UML diagram list
                self.uml_diagrams = diagrams
                self.update_uml_preview()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh UML diagrams: {str(e)}")

    def refresh_metadata(self):
        try:
            response = self.client.get("/metadata/")
            if response.status_code == 200:
                metadata = response.json()
                self.metadata_grid.delete(*self.metadata_grid.get_children())
                for item in metadata:
                    self.metadata_grid.insert('', 'end', values=(
                        item['key'],
                        item['value'],
                        item['type'],
                        "Global" if item['item_id'] is None else f"Item {item['item_id']}"
                    ))
                self.update_statistics(metadata)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh metadata: {str(e)}")

    def update_statistics(self, metadata):
        try:
            # Clear existing statistics
            self.stats_grid.delete(*self.stats_grid.get_children())
            
            # Calculate statistics
            stats = {
                "Total Models": len(self.model_listbox.get_children()),
                "Total Requirements": len(self.req_listbox.get_children()),
                "Total UML Diagrams": len(self.uml_diagrams),
                "Total Metadata Items": len(metadata),
                "Project Version": next((m['value'] for m in metadata if m['key'] == 'project_version'), 'N/A')
            }
            
            # Update statistics grid
            for key, value in stats.items():
                self.stats_grid.insert('', 'end', values=(key, value))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update statistics: {str(e)}")

    def update_uml_preview(self):
        try:
            if hasattr(self, 'uml_diagrams') and self.uml_diagrams:
                # Get the first diagram's content
                diagram = self.uml_diagrams[0]
                self.diagram_title.delete(0, tk.END)
                self.diagram_title.insert(0, diagram['title'])
                self.uml_type.set(diagram['type'])
                self.uml_content.delete('1.0', tk.END)
                self.uml_content.insert('1.0', diagram['content'])
                if diagram['model_id']:
                    self.diagram_model.set(f"Model {diagram['model_id']}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update UML preview: {str(e)}")

    def init_models_tab(self):
        # Title
        ttk.Label(self.models_tab, text="System Models Management", style="Title.TLabel").pack(pady=10)
        
        # Split into left and right panels
        paned = ttk.PanedWindow(self.models_tab, orient=tk.HORIZONTAL)
        paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left panel
        left_panel = ttk.Frame(paned)
        paned.add(left_panel, weight=1)
        
        # Model categories
        categories_frame = ttk.LabelFrame(left_panel, text="Model Categories")
        categories_frame.pack(fill='x', padx=5, pady=5)
        
        self.model_category = ttk.Combobox(categories_frame, 
            values=['System Architecture', 'Domain Model', 'Process Model', 
                   'Data Model', 'Component Model', 'Integration Model'])
        self.model_category.pack(fill='x', padx=5, pady=5)
        self.model_category.set('System Architecture')
        
        # Model list
        list_frame = ttk.LabelFrame(left_panel, text="Model List")
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.model_listbox = ttk.Treeview(list_frame, columns=('name', 'type', 'status'),
                                         show='headings')
        self.model_listbox.heading('name', text='Name')
        self.model_listbox.heading('type', text='Type')
        self.model_listbox.heading('status', text='Status')
        self.model_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        self.model_listbox.bind('<<TreeviewSelect>>', self.on_model_select)
        
        # Buttons
        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(fill='x', padx=5, pady=5)
        ttk.Button(btn_frame, text="New Model", command=self.new_model_dialog).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_models).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_model).pack(side='left', padx=5)
        
        # Right panel
        right_panel = ttk.Frame(paned)
        paned.add(right_panel, weight=2)
        
        # Model details
        details_frame = ttk.LabelFrame(right_panel, text="Model Details")
        details_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Model properties
        props_frame = ttk.Frame(details_frame)
        props_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(props_frame, text="Name:", style="Header.TLabel").grid(row=0, column=0, sticky='w', pady=2)
        self.model_name = ttk.Entry(props_frame, width=40)
        self.model_name.grid(row=0, column=1, sticky='w', pady=2)
        
        ttk.Label(props_frame, text="Category:", style="Header.TLabel").grid(row=1, column=0, sticky='w', pady=2)
        self.model_type = ttk.Entry(props_frame, width=40)
        self.model_type.grid(row=1, column=1, sticky='w', pady=2)
        
        ttk.Label(props_frame, text="Description:", style="Header.TLabel").grid(row=2, column=0, sticky='w', pady=2)
        self.model_desc = scrolledtext.ScrolledText(props_frame, height=5, width=40)
        self.model_desc.grid(row=2, column=1, sticky='w', pady=2)
        
        # Associated requirements
        req_frame = ttk.LabelFrame(details_frame, text="Associated Requirements")
        req_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.model_reqs = ttk.Treeview(req_frame, columns=('id', 'title', 'priority'),
                                      show='headings')
        self.model_reqs.heading('id', text='ID')
        self.model_reqs.heading('title', text='Title')
        self.model_reqs.heading('priority', text='Priority')
        self.model_reqs.pack(fill='both', expand=True, padx=5, pady=5)

    def init_requirements_tab(self):
        # Title
        ttk.Label(self.requirements_tab, text="Requirements Management", style="Title.TLabel").pack(pady=10)
        
        # Split into left and right panels
        paned = ttk.PanedWindow(self.requirements_tab, orient=tk.HORIZONTAL)
        paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left panel
        left_panel = ttk.Frame(paned)
        paned.add(left_panel, weight=1)
        
        # Requirement filters
        filters_frame = ttk.LabelFrame(left_panel, text="Filters")
        filters_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(filters_frame, text="Status:").pack(side='left', padx=5)
        self.req_status_filter = ttk.Combobox(filters_frame, 
            values=['All', 'New', 'In Progress', 'Completed', 'Verified'])
        self.req_status_filter.pack(side='left', padx=5)
        self.req_status_filter.set('All')
        
        ttk.Label(filters_frame, text="Priority:").pack(side='left', padx=5)
        self.req_priority_filter = ttk.Combobox(filters_frame,
            values=['All', 'High', 'Medium', 'Low'])
        self.req_priority_filter.pack(side='left', padx=5)
        self.req_priority_filter.set('All')
        
        # Requirements list
        list_frame = ttk.LabelFrame(left_panel, text="Requirements")
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.req_listbox = ttk.Treeview(list_frame, 
            columns=('id', 'title', 'status', 'priority'),
            show='headings')
        self.req_listbox.heading('id', text='ID')
        self.req_listbox.heading('title', text='Title')
        self.req_listbox.heading('status', text='Status')
        self.req_listbox.heading('priority', text='Priority')
        self.req_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        self.req_listbox.bind('<<TreeviewSelect>>', self.on_requirement_select)
        
        # Buttons
        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(fill='x', padx=5, pady=5)
        ttk.Button(btn_frame, text="New Requirement", 
                  command=self.new_requirement_dialog).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Refresh",
                  command=self.refresh_requirements).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete",
                  command=self.delete_requirement).pack(side='left', padx=5)
        
        # Right panel
        right_panel = ttk.Frame(paned)
        paned.add(right_panel, weight=2)
        
        # Requirement details
        details_frame = ttk.LabelFrame(right_panel, text="Requirement Details")
        details_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Properties
        props_frame = ttk.Frame(details_frame)
        props_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(props_frame, text="Title:", style="Header.TLabel").grid(row=0, column=0, sticky='w', pady=2)
        self.req_title = ttk.Entry(props_frame, width=60)
        self.req_title.grid(row=0, column=1, sticky='w', pady=2)
        
        ttk.Label(props_frame, text="Status:", style="Header.TLabel").grid(row=1, column=0, sticky='w', pady=2)
        self.req_status = ttk.Combobox(props_frame, 
            values=['New', 'In Progress', 'Completed', 'Verified'])
        self.req_status.grid(row=1, column=1, sticky='w', pady=2)
        
        ttk.Label(props_frame, text="Priority:", style="Header.TLabel").grid(row=2, column=0, sticky='w', pady=2)
        self.req_priority = ttk.Combobox(props_frame,
            values=['High', 'Medium', 'Low'])
        self.req_priority.grid(row=2, column=1, sticky='w', pady=2)
        
        ttk.Label(props_frame, text="Description:", style="Header.TLabel").grid(row=3, column=0, sticky='w', pady=2)
        self.req_desc = scrolledtext.ScrolledText(props_frame, height=5, width=60)
        self.req_desc.grid(row=3, column=1, sticky='w', pady=2)
        
        # Acceptance criteria
        criteria_frame = ttk.LabelFrame(details_frame, text="Acceptance Criteria")
        criteria_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.req_criteria = scrolledtext.ScrolledText(criteria_frame, height=5)
        self.req_criteria.pack(fill='both', expand=True, padx=5, pady=5)

    def init_uml_tab(self):
        # Title
        ttk.Label(self.uml_tab, text="UML Modeling", style="Title.TLabel").pack(pady=10)
        
        # Split into left and right panels
        paned = ttk.PanedWindow(self.uml_tab, orient=tk.HORIZONTAL)
        paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left panel - Diagram types and properties
        left_panel = ttk.Frame(paned)
        paned.add(left_panel, weight=1)
        
        # Diagram type selection
        type_frame = ttk.LabelFrame(left_panel, text="Diagram Type")
        type_frame.pack(fill='x', padx=5, pady=5)
        
        self.uml_type = ttk.Combobox(type_frame, 
            values=['Class Diagram', 'Sequence Diagram', 'Component Diagram',
                   'State Diagram', 'Activity Diagram', 'Use Case Diagram'])
        self.uml_type.pack(fill='x', padx=5, pady=5)
        self.uml_type.set('Class Diagram')
        
        # Diagram properties
        props_frame = ttk.LabelFrame(left_panel, text="Properties")
        props_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(props_frame, text="Title:").pack(padx=5, pady=2)
        self.diagram_title = ttk.Entry(props_frame)
        self.diagram_title.pack(fill='x', padx=5, pady=2)
        
        ttk.Label(props_frame, text="Associated Model:").pack(padx=5, pady=2)
        self.diagram_model = ttk.Combobox(props_frame)
        self.diagram_model.pack(fill='x', padx=5, pady=2)
        
        # PlantUML content
        content_frame = ttk.LabelFrame(left_panel, text="PlantUML Content")
        content_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.uml_content = scrolledtext.ScrolledText(content_frame)
        self.uml_content.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(fill='x', padx=5, pady=5)
        ttk.Button(btn_frame, text="Generate Diagram",
                  command=self.generate_uml).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Save",
                  command=self.save_uml).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Load Template",
                  command=self.load_uml_template).pack(side='left', padx=5)
        
        # Right panel - Diagram preview
        right_panel = ttk.Frame(paned)
        paned.add(right_panel, weight=2)
        
        preview_frame = ttk.LabelFrame(right_panel, text="Diagram Preview")
        preview_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.diagram_preview = ttk.Label(preview_frame, text="Diagram will appear here")
        self.diagram_preview.pack(fill='both', expand=True, padx=5, pady=5)

    def init_matrix_tab(self):
        # Title
        ttk.Label(self.matrix_tab, text="Requirements Traceability Matrix", 
                 style="Title.TLabel").pack(pady=10)
        
        # Controls
        control_frame = ttk.LabelFrame(self.matrix_tab, text="Matrix Controls")
        control_frame.pack(fill='x', padx=5, pady=5)
        
        # Filters
        filters_frame = ttk.Frame(control_frame)
        filters_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(filters_frame, text="Model:").pack(side='left', padx=5)
        self.matrix_model = ttk.Combobox(filters_frame)
        self.matrix_model.pack(side='left', padx=5)
        
        ttk.Label(filters_frame, text="Requirement Type:").pack(side='left', padx=5)
        self.matrix_req_type = ttk.Combobox(filters_frame,
            values=['All', 'Functional', 'Non-functional', 'Technical'])
        self.matrix_req_type.pack(side='left', padx=5)
        self.matrix_req_type.set('All')
        
        # Buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        ttk.Button(btn_frame, text="Generate Matrix",
                  command=self.generate_matrix).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Export to CSV",
                  command=self.export_matrix).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Print",
                  command=self.print_matrix).pack(side='left', padx=5)
        
        # Matrix view
        matrix_frame = ttk.Frame(self.matrix_tab)
        matrix_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.matrix_view = ttk.Treeview(matrix_frame, 
            columns=('requirement', 'type', 'priority', 'model', 'status'),
            show='headings')
        self.matrix_view.heading('requirement', text='Requirement')
        self.matrix_view.heading('type', text='Type')
        self.matrix_view.heading('priority', text='Priority')
        self.matrix_view.heading('model', text='Model')
        self.matrix_view.heading('status', text='Status')
        self.matrix_view.pack(fill='both', expand=True, padx=5, pady=5)

    def init_metadata_tab(self):
        # Title
        ttk.Label(self.metadata_tab, text="Metadata & Analytics", 
                 style="Title.TLabel").pack(pady=10)
        
        # Split into top and bottom panels
        paned = ttk.PanedWindow(self.metadata_tab, orient=tk.VERTICAL)
        paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Top panel - Statistics
        top_panel = ttk.Frame(paned)
        paned.add(top_panel, weight=1)
        
        stats_frame = ttk.LabelFrame(top_panel, text="Project Statistics")
        stats_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Statistics grid
        self.stats_grid = ttk.Treeview(stats_frame,
            columns=('metric', 'value'),
            show='headings')
        self.stats_grid.heading('metric', text='Metric')
        self.stats_grid.heading('value', text='Value')
        self.stats_grid.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Bottom panel - Metadata management
        bottom_panel = ttk.Frame(paned)
        paned.add(bottom_panel, weight=2)
        
        metadata_frame = ttk.LabelFrame(bottom_panel, text="Custom Metadata")
        metadata_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Metadata controls
        controls_frame = ttk.Frame(metadata_frame)
        controls_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(controls_frame, text="Key:").pack(side='left', padx=5)
        self.metadata_key = ttk.Entry(controls_frame, width=20)
        self.metadata_key.pack(side='left', padx=5)
        
        ttk.Label(controls_frame, text="Value:").pack(side='left', padx=5)
        self.metadata_value = ttk.Entry(controls_frame, width=40)
        self.metadata_value.pack(side='left', padx=5)
        
        ttk.Button(controls_frame, text="Add",
                  command=self.add_metadata).pack(side='left', padx=5)
        
        # Metadata grid
        self.metadata_grid = ttk.Treeview(metadata_frame,
            columns=('key', 'value', 'type', 'item'),
            show='headings')
        self.metadata_grid.heading('key', text='Key')
        self.metadata_grid.heading('value', text='Value')
        self.metadata_grid.heading('type', text='Type')
        self.metadata_grid.heading('item', text='Associated Item')
        self.metadata_grid.pack(fill='both', expand=True, padx=5, pady=5)

    def new_model_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("New Model")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.pack(fill='x', padx=5)
        
        ttk.Label(dialog, text="Description:").pack(pady=5)
        desc_entry = scrolledtext.ScrolledText(dialog, height=10)
        desc_entry.pack(fill='both', expand=True, padx=5)
        
        def save_model():
            try:
                response = self.client.post("/models/", json={
                    "name": name_entry.get(),
                    "description": desc_entry.get("1.0", tk.END).strip()
                })
                if response.status_code == 200:
                    messagebox.showinfo("Success", "Model created successfully")
                    self.refresh_models()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", f"Failed to create model: {response.text}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Save", command=save_model).pack(pady=10)

    def new_requirement_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("New Requirement")
        dialog.geometry("400x400")
        
        ttk.Label(dialog, text="Title:").pack(pady=5)
        title_entry = ttk.Entry(dialog)
        title_entry.pack(fill='x', padx=5)
        
        ttk.Label(dialog, text="Description:").pack(pady=5)
        desc_entry = scrolledtext.ScrolledText(dialog, height=10)
        desc_entry.pack(fill='both', expand=True, padx=5)
        
        ttk.Label(dialog, text="Priority:").pack(pady=5)
        priority = ttk.Combobox(dialog, values=['low', 'medium', 'high'])
        priority.set('medium')
        priority.pack(fill='x', padx=5)
        
        def save_requirement():
            try:
                response = self.client.post("/requirements/", json={
                    "title": title_entry.get(),
                    "description": desc_entry.get("1.0", tk.END).strip(),
                    "priority": priority.get()
                })
                if response.status_code == 200:
                    messagebox.showinfo("Success", "Requirement created successfully")
                    self.refresh_requirements()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", f"Failed to create requirement: {response.text}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Save", command=save_requirement).pack(pady=10)

    def generate_uml(self):
        diagram_type = self.uml_type.get()
        content = self.uml_content.get("1.0", tk.END).strip()
        
        try:
            if diagram_type == "Class Diagram":
                response = self.client.post("/uml/class-diagram/", json={
                    "classes": [{"content": content}]
                })
            else:
                response = self.client.post("/uml/sequence-diagram/", json={
                    "content": content
                })
            
            if response.status_code == 200:
                messagebox.showinfo("Success", "Diagram generated successfully")
            else:
                messagebox.showerror("Error", f"Failed to generate diagram: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generate_matrix(self):
        try:
            model_id = self.matrix_model.get() if self.matrix_model.get() else None
            response = self.client.get(f"/matrix/{'?model_id=' + model_id if model_id else ''}")
            
            if response.status_code == 200:
                matrix = response.json()
                self.matrix_view.delete(*self.matrix_view.get_children())
                for item in matrix:
                    self.matrix_view.insert('', 'end', values=(item['requirement_title'], item['requirement_type'], item['requirement_priority'], item['model_name'], item['requirement_status']))
            else:
                messagebox.showerror("Error", f"Failed to generate matrix: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_model(self):
        selection = self.model_listbox.selection()
        if selection:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this model?"):
                try:
                    model_id = self.model_listbox.item(selection)['values'][0]
                    response = self.client.delete(f"/models/{model_id}")
                    if response.status_code == 200:
                        self.refresh_models()
                        messagebox.showinfo("Success", "Model deleted successfully")
                    else:
                        messagebox.showerror("Error", f"Failed to delete model: {response.text}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def delete_requirement(self):
        selection = self.req_listbox.selection()
        if selection:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this requirement?"):
                try:
                    req_id = self.req_listbox.item(selection)['values'][0]
                    response = self.client.delete(f"/requirements/{req_id}")
                    if response.status_code == 200:
                        self.refresh_requirements()
                        messagebox.showinfo("Success", "Requirement deleted successfully")
                    else:
                        messagebox.showerror("Error", f"Failed to delete requirement: {response.text}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def save_uml(self):
        if not self.diagram_title.get():
            messagebox.showerror("Error", "Please enter a diagram title")
            return
            
        try:
            data = {
                "title": self.diagram_title.get(),
                "type": self.uml_type.get(),
                "content": self.uml_content.get("1.0", tk.END),
                "model_id": self.diagram_model.get() if self.diagram_model.get() else None
            }
            response = self.client.post("/uml/", json=data)
            if response.status_code == 200:
                messagebox.showinfo("Success", "UML diagram saved successfully")
            else:
                messagebox.showerror("Error", f"Failed to save diagram: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_uml_template(self):
        diagram_type = self.uml_type.get()
        if diagram_type == "Class Diagram":
            template = """@startuml
class MyClass {
    +attribute1: type
    +attribute2: type
    +method1(): returnType
}
@enduml"""
        elif diagram_type == "Sequence Diagram":
            template = """@startuml
participant User
participant System

User -> System: Request
System --> User: Response
@enduml"""
        else:
            template = "@startuml\n\n@enduml"
            
        self.uml_content.delete("1.0", tk.END)
        self.uml_content.insert("1.0", template)

    def export_matrix(self):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    # Write headers
                    headers = ['Requirement', 'Type', 'Priority', 'Model', 'Status']
                    writer.writerow(headers)
                    # Write data
                    for item in self.matrix_view.get_children():
                        values = self.matrix_view.item(item)['values']
                        writer.writerow(values)
                messagebox.showinfo("Success", "Matrix exported successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export matrix: {str(e)}")

    def print_matrix(self):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            if filename:
                # Create PDF
                doc = SimpleDocTemplate(filename, pagesize=letter)
                elements = []
                
                # Title
                elements.append(Paragraph("Requirements Traceability Matrix", 
                    getSampleStyleSheet()['Title']))
                elements.append(Spacer(1, 12))
                
                # Create table data
                data = [['Requirement', 'Type', 'Priority', 'Model', 'Status']]
                for item in self.matrix_view.get_children():
                    values = self.matrix_view.item(item)['values']
                    data.append(values)
                
                # Create table
                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 12),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(table)
                
                # Build PDF
                doc.build(elements)
                messagebox.showinfo("Success", "Matrix printed to PDF successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print matrix: {str(e)}")

    def add_metadata(self):
        key = self.metadata_key.get()
        value = self.metadata_value.get()
        
        if not key or not value:
            messagebox.showerror("Error", "Please enter both key and value")
            return
            
        try:
            data = {
                "key": key,
                "value": value,
                "type": "custom",
                "item_id": None  # Can be updated to associate with specific items
            }
            response = self.client.post("/metadata/", json=data)
            if response.status_code == 200:
                self.metadata_grid.insert('', 'end', values=(key, value, "custom", "Global"))
                self.metadata_key.delete(0, tk.END)
                self.metadata_value.delete(0, tk.END)
                messagebox.showinfo("Success", "Metadata added successfully")
            else:
                messagebox.showerror("Error", f"Failed to add metadata: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_model_select(self, event):
        selection = self.model_listbox.selection()
        if selection:
            try:
                response = self.client.get("/models/")
                if response.status_code == 200:
                    models = response.json()
                    model = models[self.model_listbox.index(selection)]
                    self.model_name.delete(0, tk.END)
                    self.model_name.insert(tk.END, model['name'])
                    self.model_type.delete(0, tk.END)
                    self.model_type.insert(tk.END, model['type'])
                    self.model_desc.delete("1.0", tk.END)
                    self.model_desc.insert(tk.END, model['description'])
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def on_requirement_select(self, event):
        selection = self.req_listbox.selection()
        if selection:
            try:
                response = self.client.get("/requirements/")
                if response.status_code == 200:
                    requirements = response.json()
                    req = requirements[self.req_listbox.index(selection)]
                    self.req_title.delete(0, tk.END)
                    self.req_title.insert(tk.END, req['title'])
                    self.req_status.set(req['status'])
                    self.req_priority.set(req['priority'])
                    self.req_desc.delete("1.0", tk.END)
                    self.req_desc.insert(tk.END, req['description'])
            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ModelBasedRequirementsGUI(root)
    root.mainloop()
