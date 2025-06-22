#!/usr/bin/env python3
"""
Onboarding Module for B3FileOrganizer
Handles first-run user onboarding, questionnaire, and naming.
"""

import os
import json
import random
from pathlib import Path
from b3fileorganizer.utils.i18n import tr, set_language

ONBOARDING_QUESTIONS = [
    {"key": "q1_subjects_fascinate", "prompt": "What subjects or topics fascinate you most?"},
    {"key": "q2_influential_art", "prompt": "What is a book, film, or artwork that deeply influenced you?"},
    {"key": "q3_skill_to_master", "prompt": "What's a skill you wish to master in the next year?"},
    {"key": "q4_proud_project", "prompt": "What's a project or creation you're most proud of?"},
    {"key": "q5_recurring_theme", "prompt": "What's a recurring theme or question in your life or work?"},
    {"key": "q6_favorite_learning", "prompt": "What's your favorite way to learn something new?"},
    {"key": "q7_breadth_vs_depth", "prompt": "Do you prefer exploring many topics or going deep into one?"},
    {"key": "q8_more_time_hobby", "prompt": "What's a hobby or passion you'd like to spend more time on?"},
    {"key": "q9_inspiring_memory", "prompt": "What's a memory that often inspires your work or creativity?"},
    {"key": "q10_returning_question", "prompt": "What's a question you keep returning to?"},
    {"key": "q11_collector_creator_connector", "prompt": "Do you see yourself as more of a collector, creator, or connector of ideas?"},
    {"key": "q12_chaos_vs_order", "prompt": "How do you feel about chaos vs. order in your workspace?"},
    {"key": "q13_deadlines_feeling", "prompt": "What's your relationship to deadlines—do they motivate or stress you?"},
    {"key": "q14_work_soundscape", "prompt": "Do you prefer to work in silence, with music, or with background noise?"},
    {"key": "q15_handle_distractions", "prompt": "How do you handle distractions or interruptions?"},
    {"key": "q16_favorite_time_of_day", "prompt": "What's your favorite time of day to do focused work?"},
    {"key": "q17_plan_or_improvise", "prompt": "Do you like to plan ahead or improvise as you go?"},
    {"key": "q18_celebrate_completion", "prompt": "How do you celebrate finishing a project or task?"},
    {"key": "q19_approach_failure", "prompt": "What's your approach to failure or mistakes?"},
    {"key": "q20_guiding_belief", "prompt": "What's a belief or value that shapes your work?"},
    {"key": "q21_workspace_description", "prompt": "How would you describe your physical workspace (tidy, cluttered, creative mess, etc.)?"},
    {"key": "q22_workspace_reorg_freq", "prompt": "How often do you clean or reorganize your workspace?"},
    {"key": "q23_workspace_change", "prompt": "What's one thing you wish you could change about your workspace?"},
    {"key": "q24_work_rituals", "prompt": "Do you use any rituals to start or end your work sessions?"},
    {"key": "q25_tools_within_reach", "prompt": "What tools or objects are always within reach when you work?"},
    {"key": "q26_capture_ideas", "prompt": "How do you keep track of ideas that come to you unexpectedly?"},
    {"key": "q27_digital_vs_analog", "prompt": "Do you prefer digital or analog tools for notes and planning?"},
    {"key": "q28_archive_old_projects", "prompt": "How do you archive or let go of old projects or materials?"},
    {"key": "q29_mark_done", "prompt": "What's your favorite way to mark something as 'done'?"},
    {"key": "q30_handle_digital_clutter", "prompt": "How do you handle digital clutter (files, emails, tabs, etc.)?"},
    {"key": "q31_when_energized", "prompt": "When do you feel most energized and creative?"},
    {"key": "q32_workday_structure", "prompt": "How do you structure your workday (blocks, sprints, flow, etc.)?"},
    {"key": "q33_breaks_how", "prompt": "Do you take regular breaks? If so, how?"},
    {"key": "q34_recharge_method", "prompt": "How do you recharge after intense work?"},
    {"key": "q35_ideal_focus_length", "prompt": "What's your ideal length for a focused work session?"},
    {"key": "q36_track_progress", "prompt": "How do you track or reflect on your progress?"},
    {"key": "q37_working_alone_or_with_others", "prompt": "Do you prefer working alone or with others (even virtually)?"},
    {"key": "q38_routine_vs_spontaneity", "prompt": "How do you balance routine and spontaneity in your work?"},
    {"key": "q39_small_habit_big_diff", "prompt": "What's a small habit that makes a big difference for you?"},
    {"key": "q40_perfect_workday", "prompt": "If you could design your perfect workday, what would it look and feel like?"}
]

SYSTEM_NAME_POOL = [
    "Athena", "Hermes", "Chronos", "Sophia", "Prometheus", "Apollo", "Artemis", "Helios", "Gaia", "Orion"
]

PROFILE_PATH = Path("config/user_profile.json")


def needs_onboarding():
    """Check if onboarding is needed (no profile or incomplete)."""
    if not PROFILE_PATH.exists():
        return True
    try:
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            profile = json.load(f)
        return not profile.get("metadata", {}).get("profile_complete", False)
    except Exception:
        return True


def run_onboarding():
    """Run the onboarding questionnaire and naming process."""
    # Language selection
    lang = input(tr("language") + " (en/de/it/es/el/ru/ar): ").strip().lower()
    if lang:
        set_language(lang)
    print("\n" + tr("welcome") + "\n")
    answers = {}
    for i, q in enumerate(ONBOARDING_QUESTIONS, 1):
        prompt = tr(q['key']) if tr(q['key']) != q['key'] else q['prompt']
        ans = input(f"({i}/{len(ONBOARDING_QUESTIONS)}) " + prompt + " ").strip()
        answers[q['key']] = ans
    print("\n" + tr("thank_you"))
    # Alias
    alias = input(tr("alias_prompt") + " ").strip()
    # System name
    sys_name = input(tr("system_name_prompt") + " ").strip()
    if not sys_name:
        sys_name = random.choice(SYSTEM_NAME_POOL)
        print(tr("system_auto_named").replace("{sys_name}", sys_name))
    # Save profile
    profile = {
        "user_info": {"alias": alias, "language": lang},
        "onboarding_answers": answers,
        "system_name": sys_name,
        "metadata": {"profile_complete": True}
    }
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROFILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    return alias, sys_name, answers


def generate_first_message(alias, sys_name, answers):
    """Generate a personalized first message exchange."""
    main_focus = answers.get("main_focus", tr("your_work"))
    top_projects = answers.get("top_projects", tr("your_projects"))
    msg = f"""
🎉 {tr('welcome_user').replace('{alias}', alias)}
{tr('im_system').replace('{sys_name}', sys_name)}

{tr('crafted_zettelkasten')}
{tr('here_to_help').replace('{main_focus}', main_focus)}

{tr('ready_to_begin')}
{tr('help_hint')}
"""
    return msg 