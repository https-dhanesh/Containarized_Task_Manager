import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");


  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await fetch('/api/tasks');
        if (response.ok) {
          const data = await response.json();
          setTasks(data);
        }
      } catch (error) {
        console.error("Error fetching tasks:", error);
      }
    };

    fetchTasks();
    const interval = setInterval(fetchTasks, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!newTask) return;

    await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: newTask }),
    });

    setNewTask("");
  };

  return (
    <div className="App" style={{ padding: "20px" }}>
      <h1>Task Manager (Dockerized)</h1>

      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input
          type="text"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          placeholder="Enter a new task..."
          style={{ padding: "10px", width: "300px" }}
        />
        <button type="submit" style={{ padding: "10px" }}>Add Task</button>
      </form>

      <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        {tasks.map((task) => (
          <div key={task.id} style={{ 
            border: "1px solid #ccc", 
            padding: "10px", 
            borderRadius: "5px",
            backgroundColor: task.status === "DONE" ? "#d4edda" : "#fff3cd"
          }}>
            <strong>#{task.id}:</strong> {task.content} 
            <span style={{ float: "right", fontWeight: "bold" }}>
              [{task.status}]
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;