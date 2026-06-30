import { useState } from "react";
import api from "../services/api";

function TaskForm({ fetchTasks }) {

    const [loading, setLoading] = useState(false);

    const [form, setForm] = useState({
        title: "",
        description: "",
        deadline: "",
        estimated_hours: "",
        priority: 3,
    });

    function handleChange(e) {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    }

    async function handleSubmit(e) {

        e.preventDefault();

        setLoading(true);

        try {

            await api.post("/tasks", {
                ...form,
                estimated_hours: Number(form.estimated_hours),
                priority: Number(form.priority),
            });

            fetchTasks();

            setForm({
                title: "",
                description: "",
                deadline: "",
                estimated_hours: "",
                priority: 3,
            });

        } catch (err) {

            console.error(err);

            alert("Failed to create task.");

        }

        setLoading(false);

    }

    return (

        <div className="bg-slate-900 border border-slate-800 rounded-2xl shadow-xl p-8">

            <h2 className="text-3xl font-bold mb-2">

                ✨ Add New Task

            </h2>

            <p className="text-slate-400 mb-8">

                Let Gemini analyze and prioritize your task.

            </p>

            <form
                onSubmit={handleSubmit}
                className="space-y-6"
            >

                <input
                    className="w-full bg-slate-800 rounded-xl p-4 outline-none focus:ring-2 focus:ring-cyan-500"
                    name="title"
                    placeholder="Task Title"
                    value={form.title}
                    onChange={handleChange}
                    required
                />

                <textarea
                    className="w-full bg-slate-800 rounded-xl p-4 outline-none focus:ring-2 focus:ring-cyan-500"
                    name="description"
                    placeholder="Description"
                    rows="4"
                    value={form.description}
                    onChange={handleChange}
                />

                <div className="grid md:grid-cols-3 gap-5">

                    <input
                        className="bg-slate-800 rounded-xl p-4 outline-none focus:ring-2 focus:ring-cyan-500"
                        type="datetime-local"
                        name="deadline"
                        value={form.deadline}
                        onChange={handleChange}
                        required
                    />

                    <input
                        className="bg-slate-800 rounded-xl p-4 outline-none focus:ring-2 focus:ring-cyan-500"
                        type="number"
                        name="estimated_hours"
                        placeholder="Hours"
                        value={form.estimated_hours}
                        onChange={handleChange}
                        required
                    />

                    <select
                        className="bg-slate-800 rounded-xl p-4 outline-none focus:ring-2 focus:ring-cyan-500"
                        name="priority"
                        value={form.priority}
                        onChange={handleChange}
                    >

                        <option value={1}>Very Low</option>
                        <option value={2}>Low</option>
                        <option value={3}>Medium</option>
                        <option value={4}>High</option>
                        <option value={5}>Very High</option>

                    </select>

                </div>

                <button
                    disabled={loading}
                    className="w-full bg-cyan-600 hover:bg-cyan-700 transition rounded-xl py-4 text-xl font-bold disabled:opacity-50"
                >

                    {loading
                        ? "🧠 Gemini is analyzing..."
                        : "✨ Analyze & Add Task"}

                </button>

            </form>

        </div>

    );

}

export default TaskForm;