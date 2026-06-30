import { useEffect, useState } from "react";
import api from "../services/api";

function TaskCard({ task, fetchTasks }) {

    const [progress, setProgress] = useState(0);

    useEffect(() => {
        setTimeout(() => {
            setProgress(task.completion_probability || 0);
        }, 150);
    }, [task]);

    const urgency = {
        Critical: "bg-red-600",
        High: "bg-orange-500",
        Medium: "bg-yellow-500 text-black",
        Low: "bg-green-600",
    };

    async function deleteTask() {

        if (!window.confirm("Delete this task?")) return;

        try {

            await api.delete(`/tasks/${task._id}`);

            fetchTasks();

        } catch {

            alert("Unable to delete.");

        }

    }

    return (

        <div className="group bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-lg hover:shadow-cyan-500/20 hover:-translate-y-1 transition-all duration-300">

            <div className="flex justify-between items-start">

                <div>

                    <h2 className="text-3xl font-bold">

                        {task.title}

                    </h2>

                    <p className="text-slate-400 mt-3 max-w-3xl">

                        {task.description}

                    </p>

                </div>

                <div className="flex gap-3">

                    <span className={`px-4 py-2 rounded-full text-sm font-bold ${urgency[task.urgency] || "bg-slate-700"}`}>

                        {task.urgency}

                    </span>

                    <span className="bg-cyan-600 px-4 py-2 rounded-full font-bold">

                        ⭐ {task.ai_priority}/10

                    </span>

                </div>

            </div>

            <div className="grid md:grid-cols-3 gap-5 mt-8">

                <Info
                    title="🧩 Complexity"
                    value={task.complexity}
                />

                <Info
                    title="⏰ Estimated Hours"
                    value={task.estimated_hours}
                />

                <Info
                    title="📅 Deadline"
                    value={new Date(task.deadline).toLocaleString()}
                />

            </div>

            <div className="mt-8">

                <div className="flex justify-between mb-3">

                    <span className="font-semibold">

                        Completion Probability

                    </span>

                    <span className="font-bold">

                        {progress}%

                    </span>

                </div>

                <div className="w-full h-4 bg-slate-700 rounded-full overflow-hidden">

                    <div
                        className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-700"
                        style={{
                            width: `${progress}%`
                        }}
                    />

                </div>

            </div>

            <div className="grid md:grid-cols-2 gap-6 mt-8">

                <div className="rounded-2xl bg-slate-800 p-6">

                    <h3 className="text-cyan-400 font-bold text-lg mb-3">

                        💡 AI Recommendation

                    </h3>

                    <p className="text-slate-300">

                        {task.recommended_start}

                    </p>

                </div>

                <div className="rounded-2xl bg-red-950 p-6">

                    <h3 className="text-red-400 font-bold text-lg mb-3">

                        ⚠ Risk Analysis

                    </h3>

                    <p className="text-slate-300">

                        {task.risk}

                    </p>

                </div>

            </div>

            <div className="flex justify-end mt-8">

                <button
                    onClick={deleteTask}
                    className="bg-red-600 hover:bg-red-700 transition px-6 py-3 rounded-xl font-semibold"
                >

                    🗑 Delete Task

                </button>

            </div>

        </div>

    );

}

function Info({ title, value }) {

    return (

        <div className="bg-slate-800 rounded-xl p-5">

            <p className="text-slate-400">

                {title}

            </p>

            <h2 className="text-xl font-bold mt-3">

                {value}

            </h2>

        </div>

    );

}

export default TaskCard;