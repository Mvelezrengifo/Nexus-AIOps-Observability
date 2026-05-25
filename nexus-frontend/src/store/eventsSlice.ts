import { StateCreator } from 'zustand';
import type { OperationalEvent } from '../types/events';

export interface EventsSlice {
  events: OperationalEvent[];
  addEvent: (event: OperationalEvent) => void;
}

export const createEventsSlice: StateCreator<EventsSlice> = (set) => ({
  events: [],
  addEvent: (event) =>
    set((state) => ({
      events: [...state.events, event].slice(-100), // mantener últimos 100 eventos
    })),
});
