"""Tests for the task priority feature.

Cover both adding a task with a priority and filtering by priority,
and check that an invalid priority raises ValueError.
"""

# Student ID: 2416130

import pytest

from taskmanager import core


def test_add_task_with_priority():
    """Test adding tasks with different priorities."""
    tasks = []
    tasks = core.add_task(tasks, "High priority task", "high")
    tasks = core.add_task(tasks, "Medium priority task", "medium")
    tasks = core.add_task(tasks, "Low priority task", "low")
    
    assert len(tasks) == 3
    assert tasks[0]["priority"] == "high"
    assert tasks[1]["priority"] == "medium"
    assert tasks[2]["priority"] == "low"


def test_add_task_default_priority():
    """Test that priority defaults to 'medium' when not specified."""
    tasks = []
    tasks = core.add_task(tasks, "Default priority task")
    
    assert tasks[0]["priority"] == "medium"


def test_add_task_invalid_priority():
    """Test that invalid priority raises ValueError."""
    tasks = []
    with pytest.raises(ValueError):
        core.add_task(tasks, "Invalid priority task", "urgent")


def test_tasks_with_priority():
    """Test filtering tasks by priority."""
    tasks = []
    tasks = core.add_task(tasks, "High 1", "high")
    tasks = core.add_task(tasks, "Medium 1", "medium")
    tasks = core.add_task(tasks, "High 2", "high")
    tasks = core.add_task(tasks, "Low 1", "low")
    
    high_tasks = core.tasks_with_priority(tasks, "high")
    assert len(high_tasks) == 2
    assert high_tasks[0]["title"] == "High 1"
    assert high_tasks[1]["title"] == "High 2"
    
    medium_tasks = core.tasks_with_priority(tasks, "medium")
    assert len(medium_tasks) == 1
    assert medium_tasks[0]["title"] == "Medium 1"
    
    low_tasks = core.tasks_with_priority(tasks, "low")
    assert len(low_tasks) == 1
    assert low_tasks[0]["title"] == "Low 1"


def test_tasks_with_priority_empty_result():
    """Test filtering returns empty list when no tasks match."""
    tasks = []
    tasks = core.add_task(tasks, "Medium task", "medium")
    
    high_tasks = core.tasks_with_priority(tasks, "high")
    assert high_tasks == []


def test_tasks_with_priority_does_not_modify_input():
    """Test that tasks_with_priority doesn't modify the input list."""
    tasks = []
    tasks = core.add_task(tasks, "High task", "high")
    tasks = core.add_task(tasks, "Medium task", "medium")
    
    original_length = len(tasks)
    core.tasks_with_priority(tasks, "high")
    
    assert len(tasks) == original_length
