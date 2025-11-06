#!/usr/bin/env node

/**
 * Task Parser and Validator
 *
 * Utilities for parsing, validating, and managing hierarchical task files.
 *
 * Usage:
 *   node parse-tasks.js --validate          # Validate all task files
 *   node parse-tasks.js --parse             # Parse and display task structure
 *   node parse-tasks.js --progress TASK-001 # Show progress for specific task
 *   node parse-tasks.js --update TASK-001   # Update parent task progress
 */

import { readFileSync, readdirSync, existsSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const PROJECT_ROOT = join(__dirname, '..', '..');
const MASTER_TASK_FILE = join(PROJECT_ROOT, '.claude', 'TASK.md');
const TASKS_DIR = join(PROJECT_ROOT, '.claude', 'tasks');

// ANSI color codes for terminal output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
};

/**
 * Parse a task line from master TASK.md
 * Format: - [ ] [TASK-001] Description (3/5) → @.claude/tasks/TASK-001-file.md
 */
function parseTaskLine(line) {
  const taskRegex = /^- \[([ x])\] \[?(TASK-\d{3})\]? (.+?)( \((\d+)\/(\d+)\))?( → @(.+))?$/;
  const match = line.trim().match(taskRegex);

  if (!match) return null;

  return {
    completed: match[1] === 'x',
    taskId: match[2],
    description: match[3].trim(),
    currentProgress: match[5] ? parseInt(match[5]) : 0,
    totalProgress: match[6] ? parseInt(match[6]) : 0,
    fileReference: match[8] || null,
    rawLine: line
  };
}

/**
 * Parse a subtask line from feature task file
 * Format: - [ ] [TASK-001.1] Subtask description
 */
function parseSubtaskLine(line) {
  const subtaskRegex = /^- \[([ x])\] \[?(TASK-\d{3}\.\d+)\]? (.+)$/;
  const match = line.trim().match(subtaskRegex);

  if (!match) return null;

  return {
    completed: match[1] === 'x',
    subtaskId: match[2],
    description: match[3].trim(),
    rawLine: line
  };
}

/**
 * Parse master TASK.md file
 */
function parseMasterTaskFile() {
  if (!existsSync(MASTER_TASK_FILE)) {
    console.error(`${colors.red}Error: Master TASK.md not found at ${MASTER_TASK_FILE}${colors.reset}`);
    process.exit(1);
  }

  const content = readFileSync(MASTER_TASK_FILE, 'utf-8');
  const lines = content.split('\n');

  const tasks = {
    inProgress: [],
    pending: [],
    completed: []
  };

  let currentSection = null;

  for (const line of lines) {
    if (line.includes('## In Progress')) {
      currentSection = 'inProgress';
    } else if (line.includes('## Pending')) {
      currentSection = 'pending';
    } else if (line.includes('## Completed')) {
      currentSection = 'completed';
    } else if (currentSection && line.trim().startsWith('- [')) {
      const task = parseTaskLine(line);
      if (task) {
        tasks[currentSection].push(task);
      }
    }
  }

  return tasks;
}

/**
 * Parse a feature task file
 */
function parseFeatureTaskFile(filePath) {
  if (!existsSync(filePath)) {
    return null;
  }

  const content = readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');

  const task = {
    title: '',
    status: 'Unknown',
    prp: null,
    started: null,
    completed: null,
    subtasks: [],
    completionCount: 0,
    totalCount: 0,
    filePath
  };

  let inSubtasksSection = false;

  for (const line of lines) {
    // Parse title
    if (line.startsWith('# [TASK-')) {
      task.title = line.replace(/^# /, '').trim();
    }

    // Parse metadata
    if (line.startsWith('**Status**:')) {
      task.status = line.replace('**Status**:', '').trim();
    }
    if (line.startsWith('**PRP**:')) {
      task.prp = line.replace('**PRP**:', '').trim();
    }
    if (line.startsWith('**Started**:')) {
      task.started = line.replace('**Started**:', '').trim();
    }
    if (line.startsWith('**Completed**:')) {
      task.completed = line.replace('**Completed**:', '').trim();
    }

    // Parse subtasks
    if (line.includes('## Subtasks')) {
      inSubtasksSection = true;
      continue;
    }

    if (inSubtasksSection && line.trim().startsWith('- [')) {
      const subtask = parseSubtaskLine(line);
      if (subtask) {
        task.subtasks.push(subtask);
        if (subtask.completed) {
          task.completionCount++;
        }
      }
    } else if (inSubtasksSection && line.startsWith('## ')) {
      inSubtasksSection = false;
    }
  }

  task.totalCount = task.subtasks.length;

  return task;
}

/**
 * Calculate progress for a task
 */
function calculateProgress(taskId) {
  const masterTasks = parseMasterTaskFile();
  const allTasks = [...masterTasks.inProgress, ...masterTasks.pending, ...masterTasks.completed];
  const masterTask = allTasks.find(t => t.taskId === taskId);

  if (!masterTask) {
    console.error(`${colors.red}Error: Task ${taskId} not found in master TASK.md${colors.reset}`);
    return null;
  }

  if (!masterTask.fileReference) {
    console.log(`${colors.yellow}Warning: Task ${taskId} has no feature file reference${colors.reset}`);
    return {
      taskId,
      completed: 0,
      total: 0,
      percentage: 0
    };
  }

  const featureFilePath = join(PROJECT_ROOT, masterTask.fileReference.replace('@', '').replace(/\//g, '\\'));
  const featureTask = parseFeatureTaskFile(featureFilePath);

  if (!featureTask) {
    console.error(`${colors.red}Error: Feature file not found at ${featureFilePath}${colors.reset}`);
    return null;
  }

  const percentage = featureTask.totalCount > 0
    ? Math.round((featureTask.completionCount / featureTask.totalCount) * 100)
    : 0;

  return {
    taskId,
    description: masterTask.description,
    completed: featureTask.completionCount,
    total: featureTask.totalCount,
    percentage,
    status: featureTask.status,
    subtasks: featureTask.subtasks
  };
}

/**
 * Update parent task progress in master TASK.md
 */
function updateParentTaskProgress(taskId) {
  const progress = calculateProgress(taskId);

  if (!progress) {
    return false;
  }

  const content = readFileSync(MASTER_TASK_FILE, 'utf-8');
  const lines = content.split('\n');

  let updated = false;
  const taskIdPattern = `[${taskId}]`;

  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes(taskIdPattern)) {
      const task = parseTaskLine(lines[i]);
      if (task && task.taskId === taskId) {
        // Check if all subtasks are complete
        const allComplete = progress.completed === progress.total && progress.total > 0;
        const checkbox = allComplete ? 'x' : ' ';

        // Reconstruct task line
        const fileRef = task.fileReference ? ` → @${task.fileReference}` : '';
        const progressText = progress.total > 0 ? ` (${progress.completed}/${progress.total})` : '';

        lines[i] = `- [${checkbox}] [${taskId}] ${task.description}${progressText}${fileRef}`;
        updated = true;

        console.log(`${colors.green}✓ Updated ${taskId}: ${progress.completed}/${progress.total} complete${colors.reset}`);

        // If all complete, move to Completed section
        if (allComplete && !task.completed) {
          console.log(`${colors.cyan}→ All subtasks complete! Moving ${taskId} to Completed section...${colors.reset}`);
          // Remove from current position
          const taskLine = lines.splice(i, 1)[0];

          // Find Completed section
          const completedIndex = lines.findIndex(line => line.includes('## Completed'));
          if (completedIndex !== -1) {
            // Insert after ## Completed line
            lines.splice(completedIndex + 1, 0, taskLine);
            console.log(`${colors.green}✓ Moved ${taskId} to Completed section${colors.reset}`);
          }
        }

        break;
      }
    }
  }

  if (updated) {
    writeFileSync(MASTER_TASK_FILE, lines.join('\n'), 'utf-8');
    console.log(`${colors.green}✓ Master TASK.md updated successfully${colors.reset}`);
    return true;
  }

  console.error(`${colors.red}Error: Failed to update ${taskId} in master TASK.md${colors.reset}`);
  return false;
}

/**
 * Validate all task files
 */
function validateTasks() {
  console.log(`${colors.bright}${colors.blue}=== Task Validation ===${colors.reset}\n`);

  const errors = [];
  const warnings = [];

  // 1. Validate master TASK.md exists
  if (!existsSync(MASTER_TASK_FILE)) {
    errors.push('Master TASK.md not found');
    console.error(`${colors.red}✗ Master TASK.md not found${colors.reset}`);
    return { errors, warnings, valid: false };
  }
  console.log(`${colors.green}✓ Master TASK.md found${colors.reset}`);

  // 2. Parse master TASK.md
  const masterTasks = parseMasterTaskFile();
  const allTasks = [...masterTasks.inProgress, ...masterTasks.pending, ...masterTasks.completed];
  console.log(`${colors.green}✓ Parsed ${allTasks.length} tasks from master TASK.md${colors.reset}`);

  // 3. Validate task IDs are unique
  const taskIds = new Set();
  for (const task of allTasks) {
    if (taskIds.has(task.taskId)) {
      errors.push(`Duplicate task ID: ${task.taskId}`);
      console.error(`${colors.red}✗ Duplicate task ID: ${task.taskId}${colors.reset}`);
    }
    taskIds.add(task.taskId);
  }

  if (taskIds.size === allTasks.length) {
    console.log(`${colors.green}✓ All task IDs are unique${colors.reset}`);
  }

  // 4. Validate task ID format (TASK-XXX)
  for (const task of allTasks) {
    if (!/^TASK-\d{3}$/.test(task.taskId)) {
      errors.push(`Invalid task ID format: ${task.taskId} (expected TASK-XXX)`);
      console.error(`${colors.red}✗ Invalid task ID format: ${task.taskId}${colors.reset}`);
    }
  }

  // 5. Validate file references exist
  for (const task of allTasks) {
    if (task.fileReference) {
      const filePath = join(PROJECT_ROOT, task.fileReference.replace('@', '').replace(/\//g, '\\'));
      if (!existsSync(filePath)) {
        errors.push(`File not found: ${task.fileReference} (task ${task.taskId})`);
        console.error(`${colors.red}✗ File not found: ${task.fileReference}${colors.reset}`);
      } else {
        // Validate feature task file
        const featureTask = parseFeatureTaskFile(filePath);
        if (featureTask) {
          // Check if progress counts match
          if (task.currentProgress !== featureTask.completionCount ||
              task.totalProgress !== featureTask.totalCount) {
            warnings.push(`Progress mismatch for ${task.taskId}: master shows ${task.currentProgress}/${task.totalProgress}, file shows ${featureTask.completionCount}/${featureTask.totalCount}`);
            console.log(`${colors.yellow}⚠ Progress mismatch for ${task.taskId}${colors.reset}`);
          }

          // Validate subtask IDs
          for (const subtask of featureTask.subtasks) {
            const expectedPrefix = `${task.taskId}.`;
            if (!subtask.subtaskId.startsWith(expectedPrefix)) {
              errors.push(`Invalid subtask ID: ${subtask.subtaskId} (expected to start with ${expectedPrefix})`);
              console.error(`${colors.red}✗ Invalid subtask ID: ${subtask.subtaskId}${colors.reset}`);
            }
          }
        }
      }
    } else {
      warnings.push(`Task ${task.taskId} has no feature file reference`);
      console.log(`${colors.yellow}⚠ Task ${task.taskId} has no feature file reference${colors.reset}`);
    }
  }

  // 6. Check for orphaned task files
  if (existsSync(TASKS_DIR)) {
    const taskFiles = readdirSync(TASKS_DIR).filter(f => f.endsWith('.md') && f !== 'README.md');
    const referencedFiles = allTasks
      .filter(t => t.fileReference)
      .map(t => t.fileReference.split('/').pop());

    for (const file of taskFiles) {
      if (!referencedFiles.includes(file)) {
        warnings.push(`Orphaned task file: ${file} (not referenced in master TASK.md)`);
        console.log(`${colors.yellow}⚠ Orphaned task file: ${file}${colors.reset}`);
      }
    }
  }

  // Summary
  console.log(`\n${colors.bright}=== Validation Summary ===${colors.reset}`);
  console.log(`Tasks validated: ${allTasks.length}`);
  console.log(`Errors: ${colors.red}${errors.length}${colors.reset}`);
  console.log(`Warnings: ${colors.yellow}${warnings.length}${colors.reset}`);

  const valid = errors.length === 0;
  if (valid) {
    console.log(`\n${colors.green}${colors.bright}✓ All validations passed!${colors.reset}`);
  } else {
    console.log(`\n${colors.red}${colors.bright}✗ Validation failed with ${errors.length} error(s)${colors.reset}`);
  }

  return { errors, warnings, valid };
}

/**
 * Display task structure
 */
function displayTaskStructure() {
  console.log(`${colors.bright}${colors.blue}=== Task Structure ===${colors.reset}\n`);

  const masterTasks = parseMasterTaskFile();

  function displaySection(title, tasks) {
    if (tasks.length === 0) return;

    console.log(`${colors.bright}${title}${colors.reset}`);
    for (const task of tasks) {
      const checkbox = task.completed ? '☑' : '☐';
      const progressBar = task.totalProgress > 0
        ? ` ${colors.cyan}(${task.currentProgress}/${task.totalProgress})${colors.reset}`
        : '';
      console.log(`  ${checkbox} ${colors.bright}[${task.taskId}]${colors.reset} ${task.description}${progressBar}`);

      if (task.fileReference) {
        console.log(`    ${colors.blue}→ ${task.fileReference}${colors.reset}`);
      }
    }
    console.log('');
  }

  displaySection('In Progress:', masterTasks.inProgress);
  displaySection('Pending:', masterTasks.pending);
  displaySection('Completed:', masterTasks.completed);
}

/**
 * Display progress for a specific task
 */
function displayProgress(taskId) {
  const progress = calculateProgress(taskId);

  if (!progress) {
    process.exit(1);
  }

  console.log(`${colors.bright}${colors.blue}=== Progress for ${taskId} ===${colors.reset}\n`);
  console.log(`${colors.bright}${progress.description}${colors.reset}`);
  console.log(`Status: ${progress.status}`);
  console.log(`Progress: ${progress.completed}/${progress.total} (${progress.percentage}%)`);
  console.log('');

  if (progress.subtasks.length > 0) {
    console.log(`${colors.bright}Subtasks:${colors.reset}`);
    for (const subtask of progress.subtasks) {
      const checkbox = subtask.completed ? `${colors.green}☑${colors.reset}` : `${colors.yellow}☐${colors.reset}`;
      console.log(`  ${checkbox} [${subtask.subtaskId}] ${subtask.description}`);
    }
  }
}

/**
 * Main CLI entry point
 */
function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('Task Parser and Validator');
    console.log('');
    console.log('Usage:');
    console.log('  node parse-tasks.js --validate          # Validate all task files');
    console.log('  node parse-tasks.js --parse             # Parse and display task structure');
    console.log('  node parse-tasks.js --progress TASK-001 # Show progress for specific task');
    console.log('  node parse-tasks.js --update TASK-001   # Update parent task progress');
    process.exit(0);
  }

  const command = args[0];

  switch (command) {
    case '--validate':
      const result = validateTasks();
      process.exit(result.valid ? 0 : 1);

    case '--parse':
      displayTaskStructure();
      break;

    case '--progress':
      if (args.length < 2) {
        console.error(`${colors.red}Error: Task ID required${colors.reset}`);
        console.log('Usage: node parse-tasks.js --progress TASK-001');
        process.exit(1);
      }
      displayProgress(args[1]);
      break;

    case '--update':
      if (args.length < 2) {
        console.error(`${colors.red}Error: Task ID required${colors.reset}`);
        console.log('Usage: node parse-tasks.js --update TASK-001');
        process.exit(1);
      }
      const success = updateParentTaskProgress(args[1]);
      process.exit(success ? 0 : 1);

    default:
      console.error(`${colors.red}Error: Unknown command: ${command}${colors.reset}`);
      process.exit(1);
  }
}

// Run if called directly
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}

// Export functions for use as module
export {
  parseMasterTaskFile,
  parseFeatureTaskFile,
  calculateProgress,
  updateParentTaskProgress,
  validateTasks
};
