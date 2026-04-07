# Spec

## Product

Habit Tracker PWA

## Source Idea

A habit tracker for my phone that lets me add daily habits, check them off quickly, and see streaks without needing my laptop runtime.

## Delivery Target

Installable PWA.

## Core User Stories

- As the primary user, I can add a habit from my phone in a few seconds.
- As the primary user, I can mark a habit complete for today with one tap.
- As the primary user, I can see my streaks without opening my laptop.

## Functional Requirements

- add and delete habits
- persist habits locally on the device
- track daily completion by date
- show completed count for today
- show best streak per habit summary
- expose installability metadata through a manifest and service worker

## Non-Functional Requirements

- mobile-first layout
- static hosting compatible
- local-first data model
- fast load on mobile
