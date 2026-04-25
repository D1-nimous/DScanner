// To-Do List Application with Local Storage

class TodoApp {
    constructor() {
        // DOM Elements
        this.taskInput = document.getElementById('taskInput');
        this.addBtn = document.getElementById('addBtn');
        this.tasksList = document.getElementById('tasksList');
        this.emptyState = document.getElementById('emptyState');
        this.dateDisplay = document.getElementById('dateDisplay');
        this.totalTasksDisplay = document.getElementById('totalTasks');
        this.completedTasksDisplay = document.getElementById('completedTasks');
        this.remainingTasksDisplay = document.getElementById('remainingTasks');
        this.clearCompletedBtn = document.getElementById('clearCompletedBtn');
        this.deleteAllBtn = document.getElementById('deleteAllBtn');
        this.filterButtons = document.querySelectorAll('.filter-btn');
        
        // State
        this.tasks = [];
        this.currentFilter = 'all';
        this.storageKey = 'todoAppTasks';
        
        // Initialize
        this.init();
    }
    
    init() {
        this.loadTasks();
        this.setupEventListeners();
        this.displayDate();
        this.render();
    }
    
    setupEventListeners() {
        // Add task
        this.addBtn.addEventListener('click', () => this.addTask());
        this.taskInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addTask();
        });
        
        // Filter buttons
        this.filterButtons.forEach(btn => {
            btn.addEventListener('click', (e) => this.setFilter(e.target.dataset.filter));
        });
        
        // Action buttons
        this.clearCompletedBtn.addEventListener('click', () => this.clearCompleted());
        this.deleteAllBtn.addEventListener('click', () => this.deleteAll());
    }
    
    displayDate() {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        const today = new Date().toLocaleDateString('en-US', options);
        this.dateDisplay.textContent = today;
    }
    
    addTask() {
        const text = this.taskInput.value.trim();
        
        if (!text) {
            alert('Please enter a task!');
            this.taskInput.focus();
            return;
        }
        
        const task = {
            id: Date.now(),
            text: text,
            completed: false,
            createdAt: new Date().toLocaleString()
        };
        
        this.tasks.unshift(task);
        this.saveTasks();
        this.taskInput.value = '';
        this.taskInput.focus();
        this.render();
    }
    
    deleteTask(id) {
        if (confirm('Are you sure you want to delete this task?')) {
            this.tasks = this.tasks.filter(task => task.id !== id);
            this.saveTasks();
            this.render();
        }
    }
    
    toggleTask(id) {
        const task = this.tasks.find(t => t.id === id);
        if (task) {
            task.completed = !task.completed;
            this.saveTasks();
            this.render();
        }
    }
    
    editTask(id) {
        const task = this.tasks.find(t => t.id === id);
        if (!task) return;
        
        const newText = prompt('Edit your task:', task.text);
        if (newText && newText.trim()) {
            task.text = newText.trim();
            this.saveTasks();
            this.render();
        }
    }
    
    setFilter(filter) {
        this.currentFilter = filter;
        
        // Update active button
        this.filterButtons.forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.filter === filter) {
                btn.classList.add('active');
            }
        });
        
        this.render();
    }
    
    getFilteredTasks() {
        switch (this.currentFilter) {
            case 'active':
                return this.tasks.filter(task => !task.completed);
            case 'completed':
                return this.tasks.filter(task => task.completed);
            default:
                return this.tasks;
        }
    }
    
    clearCompleted() {
        const completedCount = this.tasks.filter(t => t.completed).length;
        if (completedCount === 0) {
            alert('No completed tasks to clear!');
            return;
        }
        
        if (confirm(`Clear ${completedCount} completed task(s)?`)) {
            this.tasks = this.tasks.filter(task => !task.completed);
            this.saveTasks();
            this.render();
        }
    }
    
    deleteAll() {
        if (this.tasks.length === 0) {
            alert('No tasks to delete!');
            return;
        }
        
        if (confirm('Are you sure you want to delete ALL tasks? This cannot be undone!')) {
            this.tasks = [];
            this.saveTasks();
            this.render();
        }
    }
    
    updateStats() {
        const total = this.tasks.length;
        const completed = this.tasks.filter(t => t.completed).length;
        const remaining = total - completed;
        
        this.totalTasksDisplay.textContent = total;
        this.completedTasksDisplay.textContent = completed;
        this.remainingTasksDisplay.textContent = remaining;
    }
    
    render() {
        this.updateStats();
        this.renderTasks();
    }
    
    renderTasks() {
        const filteredTasks = this.getFilteredTasks();
        this.tasksList.innerHTML = '';
        
        if (filteredTasks.length === 0) {
            this.emptyState.classList.remove('hidden');
            return;
        }
        
        this.emptyState.classList.add('hidden');
        
        filteredTasks.forEach(task => {
            const li = document.createElement('li');
            li.className = `task-item ${task.completed ? 'completed' : ''}`;
            li.innerHTML = `
                <input 
                    type="checkbox" 
                    class="task-checkbox" 
                    ${task.completed ? 'checked' : ''}
                    onchange="app.toggleTask(${task.id})"
                >
                <span class="task-text">${this.escapeHtml(task.text)}</span>
                <span class="task-date">${task.createdAt}</span>
                <div class="task-actions">
                    <button class="task-btn edit-btn" onclick="app.editTask(${task.id})">Edit</button>
                    <button class="task-btn delete-btn" onclick="app.deleteTask(${task.id})">Delete</button>
                </div>
            `;
            this.tasksList.appendChild(li);
        });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    saveTasks() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.tasks));
    }
    
    loadTasks() {
        const saved = localStorage.getItem(this.storageKey);
        if (saved) {
            try {
                this.tasks = JSON.parse(saved);
            } catch (e) {
                console.error('Error loading tasks:', e);
                this.tasks = [];
            }
        }
    }
    
    // Development helper
    exportTasks() {
        const dataStr = JSON.stringify(this.tasks, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `tasks_${new Date().toISOString()}.json`;
        link.click();
    }
    
    importTasks(jsonString) {
        try {
            const imported = JSON.parse(jsonString);
            if (Array.isArray(imported)) {
                this.tasks = [...this.tasks, ...imported];
                this.saveTasks();
                this.render();
                return true;
            }
        } catch (e) {
            console.error('Error importing tasks:', e);
        }
        return false;
    }
}

// Initialize app when DOM is loaded
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new TodoApp();
});
