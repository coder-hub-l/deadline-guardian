import { useEffect, useState } from "react";
import api from "../services/api";
import TaskForm from "frontend/src/components/TaskForm";
import TaskCard from "frontend/src/components/TaskCard";

function Dashboard() {
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(false);
    const [showForm, setShowForm] = useState(false);

    useEffect(() => {
        fetchTasks();
    }, []);

    async function fetchTasks() {
        setLoading(true);

        try {
            const response = await api.get("/tasks");
            setTasks(response.data);
        } catch (err) {
            console.error(err);
        }

        setLoading(false);
    }

    const totalTasks = tasks.length;

    const criticalTasks = tasks.filter(
        task => task.urgency === "Critical"
    ).length;

    const highTasks = tasks.filter(
        task => task.urgency === "High"
    ).length;

    const avgScore =
        totalTasks === 0
            ? 0
            : (
                tasks.reduce(
                    (sum, task) => sum + (task.ai_priority || 0),
                    0
                ) / totalTasks
            ).toFixed(1);

    const topTask =
        [...tasks].sort(
            (a, b) => (b.ai_priority || 0) - (a.ai_priority || 0)
        )[0];

    return (
        <div className="min-h-screen bg-slate-950 text-white">

            <div className="max-w-7xl mx-auto px-8 py-10">

                {/* HEADER */}

                <div className="flex items-center justify-between">

                    <div>

                        <h1 className="text-5xl font-bold">
                            🧠 Deadline Guardian
                        </h1>

                        <p className="text-slate-400 mt-2 text-lg">
                            AI Powered Productivity Assistant
                        </p>

                    </div>

                    <button
                        onClick={() => setShowForm(true)}
                        className="bg-cyan-600 hover:bg-cyan-700 transition-all duration-300 px-6 py-3 rounded-xl text-lg font-semibold shadow-lg hover:scale-105"
                    >
                        ✨ Add Task
                    </button>

                </div>

                {/* STATS */}

                <div className="grid md:grid-cols-4 gap-6 mt-10">

                    <StatCard
                        title="📋 Total Tasks"
                        value={totalTasks}
                    />

                    <StatCard
                        title="🔥 Critical"
                        value={criticalTasks}
                    />

                    <StatCard
                        title="⚡ High"
                        value={highTasks}
                    />

                    <StatCard
                        title="⭐ Avg AI"
                        value={avgScore}
                    />

                </div>

                {/* AI FOCUS */}

                {topTask && (

                    <div className="mt-8 rounded-2xl bg-linear-to-r from-cyan-600 to-blue-700 p-8 shadow-xl">

                        <h2 className="text-2xl font-bold">
                            🧠 Today's AI Focus
                        </h2>

                        <p className="text-3xl font-semibold mt-3">
                            {topTask.title}
                        </p>

                        <p className="mt-4 opacity-90">
                            {topTask.reason}
                        </p>

                    </div>

                )}

                {/* FORM */}

                {showForm && (

                    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50">

                        <div className="w-full max-w-3xl relative">

                            <button
                                onClick={() => setShowForm(false)}
                                className="absolute right-4 top-4 text-2xl hover:text-red-500"
                            >
                                ✖
                            </button>

                            <TaskForm
                                fetchTasks={() => {
                                    fetchTasks();
                                    setShowForm(false);
                                }}
                            />

                        </div>

                    </div>

                )}

                {/* TASKS */}

                <div className="mt-12">

                    <h2 className="text-3xl font-bold mb-6">
                        Your Tasks
                    </h2>

                    {loading ? (

                        <div className="text-center py-20 text-xl text-slate-400">

                            🧠 Gemini is analyzing...

                        </div>

                    ) : tasks.length === 0 ? (

                        <div className="bg-slate-900 rounded-2xl p-12 text-center">

                            <h3 className="text-2xl font-semibold">
                                No Tasks Yet
                            </h3>

                            <p className="text-slate-400 mt-3">
                                Create your first task using AI.
                            </p>

                        </div>

                    ) : (

                        <div className="space-y-6">

                            {tasks.map(task => (

                                <TaskCard
                                    key={task._id}
                                    task={task}
                                    fetchTasks={fetchTasks}
                                />

                            ))}

                        </div>

                    )}

                </div>

            </div>

        </div>
    );
}

function StatCard({ title, value }) {
    return (

        <div className="bg-slate-900 rounded-2xl p-6 shadow-lg border border-slate-800">

            <p className="text-slate-400 text-lg">
                {title}
            </p>

            <h2 className="text-4xl font-bold mt-3">
                {value}
            </h2>

        </div>

    );
}

export default Dashboard;