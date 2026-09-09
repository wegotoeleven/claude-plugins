---
name: hol-up
description: "Re-explain your immediately preceding response, tailored to whatever audience the user names. Use when the user says 'hol up', 'hold up', 'wait what', 'in simple terms', 'explain that simpler', 'you lost me', or asks for the last message explained for a specific person or audience (e.g. 'hol up, for my manager', 'hol up like I'm 5', 'break that down for my mom'). With no audience named, default to a plain, jargon-free explanation for an intelligent adult with no background in the topic."
user-invocable: true
---

# Hol Up

Re-explain your own immediately preceding response — never the user's message that triggered this skill — tailored to the audience the user names, or a plain-adult default if they don't.

## Step 1: Identify the Source

The material to re-explain is always your last assistant message in this conversation. Understand its essential "what" and "why" before translating — for code, know what it does and why, not just its syntax.

## Step 2: Identify the Audience

Parse the triggering message for an explicit audience. If none is named, default to: **plain, jargon-free, for an intelligent adult with no background in the topic** — simple, never childish.

If an audience is named, it falls into one of these categories:

### Ages
| Audience | Style |
|----------|-------|
| Age 5 | Super simple words. Fun analogies with toys, animals, candy, playground. Short sentences. |
| Age 10 | Elementary level. Basic cause-and-effect. School, sports, video game analogies. |
| Age 15 | Teenager. Some abstraction OK. Social media, phone, gaming references. Slightly casual. |
| Age 20-30 | Young adult. Clear and direct. Daily-life, work, money analogies. |
| Age 40+ | Mature adult. Respectful tone. Home-ownership, career, family analogies. |

### Grade / Education Levels
| Audience | Style |
|----------|-------|
| 5th grade | Simple vocabulary, concrete examples, no jargon. |
| Middle school | Basic terminology with definitions. Step-by-step logic. |
| Senior High | Moderate complexity. Proper terms, explained. |
| College student | Academic framing. Technical terms with brief context. |
| Graduate school | Strong foundational knowledge assumed. Nuance, trade-offs, edge cases. |

### Job Roles
| Audience | They care about... | Frame around... |
|----------|--------------------|------------------|
| Manager | Impact, timeline, risk, cost | Business outcomes, decisions to be made |
| Engineer | How it works, trade-offs | Implementation, performance, maintainability |
| Designer | UX, visual impact, flow | Effect on the user, interaction patterns |
| Director | Strategy, ROI | Big picture, resource allocation |
| Product Manager | User value, priorities, scope | Feature impact, build-vs-skip |

### Relationships
| Audience | Tone | Analogy style |
|----------|------|----------------|
| Partner | Warm, conversational, patient | Household tasks, shared routines |
| Parent | Respectful, clear, no condescension | Familiar technology, home analogies |
| Kids | Playful, encouraging, short | Games, cartoons, school, animals |
| Friend | Casual, maybe humorous | Pop culture, "you know how..." |

## Step 3: Craft the Explanation

### Structure
1. **Lead with the "what"** — one sentence capturing the core point.
2. **Use an analogy** — connect to something the audience already knows.
3. **Layer in detail** — only as much as the audience level warrants.
4. **Close with the "so what"** — why this matters to them specifically.

### Language Calibration
- **Simple audiences** (young ages, non-technical roles, family, or the no-audience-named default): zero jargon — define immediately if a term is unavoidable. One idea per sentence. Concrete over abstract ("the server is like a waiter" beats "handles client-server communication").
- **Technical audiences** (engineers, grad students): proper terminology is fine — they'd feel patronized without it. Focus on trade-offs and design decisions. Stay concise.
- **Business audiences** (managers, directors): lead with impact and outcomes, quantify where possible, skip implementation details unless asked.

### Tone
Never condescending, at any level — a 5-year-old explanation should feel delightful, not dumbed-down; a manager explanation should feel empowering, not dismissive of their intelligence. Replace the technical version, don't append the plain one after it "for context." Ruthless simplification beats completeness — 80% accuracy with full comprehension beats 100% accuracy that loses the reader.

## Examples

**User says**: "hol up"
**Audience**: default (plain adult)
**Style**: Strip all jargon, one short sentence per idea, one everyday analogy, end with why it matters.

**User says**: "hol up, for my manager"
**Audience**: Manager
**Style**: "That change means requests will fail less often during peak hours. It's about two days of engineering time. I'd recommend..."

**User says**: "hol up like I'm 5"
**Audience**: Age 5
**Style**: "Imagine your toys are in a huge messy box. The thing I built is like sorting them into labeled bins so you can find your favorite one fast."
