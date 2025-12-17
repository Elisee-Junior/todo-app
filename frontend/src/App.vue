<script setup>
import { onMounted, reactive } from "vue";

const API = "/api/todos";

const state = reactive({
  todos: [],
  newTitle: "",
  loading: false,
  error: "",
});

onMounted(fetchTodos);

async function fetchTodos() {
  state.error = "";
  try {
    const res = await fetch(API);
    if (!res.ok) {
      throw new Error("Impossible de charger les tâches");
    }
    state.todos = await res.json();
  } catch (err) {
    state.error = err.message;
  }
}

async function addTodo() {
  const title = state.newTitle.trim();
  if (!title) return;

  state.loading = true;
  state.error = "";
  try {
    const res = await fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });

    if (!res.ok) {
      const { error } = await res.json();
      throw new Error(error || "Erreur serveur");
    }

    const todo = await res.json();
    state.todos.push(todo);
    state.newTitle = "";
  } catch (err) {
    state.error = err.message;
  } finally {
    state.loading = false;
  }
}

async function toggle(todo) {
  const desired = todo.completed;
  const rollback = !desired;

  state.loading = true;
  state.error = "";
  try {
    const res = await fetch(`${API}/${todo.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed: desired }),
    });

    if (!res.ok) {
      const { error } = await res.json();
      throw new Error(error || "Erreur serveur");
    }

    const updated = await res.json();
    Object.assign(todo, updated);
  } catch (err) {
    state.error = err.message;
    todo.completed = rollback;
  } finally {
    state.loading = false;
  }
}

async function remove(todo) {
  state.loading = true;
  state.error = "";

  try {
    const res = await fetch(`${API}/${todo.id}`, { method: "DELETE" });

    if (!res.ok) {
      const { error } = await res.json();
      throw new Error(error || "Erreur serveur");
    }

    state.todos = state.todos.filter((t) => t.id !== todo.id);
  } catch (err) {
    state.error = err.message;
  } finally {
    state.loading = false;
  }
}
</script>

<template>
  <main class="flex min-h-screen items-center justify-center px-4 py-10">
    <section
      class="w-full max-w-3xl rounded-2xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl backdrop-blur"
    >
      <div class="mb-6 flex items-start justify-between gap-4">
        <div>
          <p class="text-xs uppercase tracking-[0.15em] text-slate-400">
            Flask API • Vite + Vue 3 • Tailwind
          </p>
          <h1 class="mt-2 text-2xl font-semibold text-white">Todo rapide</h1>
          <p class="text-sm text-slate-300">Stockage en mémoire côté backend.</p>
        </div>
        <button
          class="rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-sm font-semibold text-slate-100 transition hover:border-sky-400 hover:text-sky-200"
          :disabled="state.loading"
          @click="fetchTodos"
        >
          Rafraîchir
        </button>
      </div>

      <form @submit.prevent="addTodo" class="mb-4 flex flex-col gap-3 sm:flex-row">
        <input
          v-model="state.newTitle"
          type="text"
          placeholder="Ajouter une tâche..."
          class="w-full rounded-xl border border-slate-700 bg-slate-800/70 px-4 py-3 text-slate-100 shadow-inner outline-none transition focus:border-sky-400 focus:ring-2 focus:ring-sky-500/40"
          :disabled="state.loading"
        />
        <button
          type="submit"
          class="w-full rounded-xl bg-gradient-to-br from-sky-400 to-indigo-500 px-4 py-3 text-sm font-bold text-slate-950 shadow-lg shadow-indigo-900/40 transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-60 sm:w-auto"
          :disabled="state.loading || !state.newTitle.trim()"
        >
          Ajouter
        </button>
      </form>

      <p v-if="state.error" class="mb-4 text-sm text-rose-300">{{ state.error }}</p>

      <div
        v-if="!state.todos.length"
        class="flex items-center justify-center rounded-xl border border-dashed border-slate-700 bg-slate-800/40 p-8 text-slate-400"
      >
        Rien à faire pour l'instant 🚀
      </div>

      <ul v-else class="space-y-3">
        <li
          v-for="todo in state.todos"
          :key="todo.id"
          class="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-800/70 p-4 transition hover:border-sky-400/50"
        >
          <input
            v-model="todo.completed"
            type="checkbox"
            class="h-5 w-5 cursor-pointer rounded border-slate-600 text-sky-400 focus:ring-sky-500"
            @change="toggle(todo)"
          />
          <div class="flex-1">
            <p
              class="text-base font-medium text-slate-100"
              :class="{ 'line-through text-slate-500': todo.completed }"
            >
              {{ todo.title }}
            </p>
          </div>
          <button
            class="rounded-lg border border-rose-500/40 bg-rose-500/15 px-3 py-2 text-xs font-semibold text-rose-100 transition hover:border-rose-300 hover:text-rose-50 disabled:cursor-not-allowed disabled:opacity-50"
            :disabled="state.loading"
            @click="remove(todo)"
          >
            Supprimer
          </button>
        </li>
      </ul>
    </section>
  </main>
</template>

