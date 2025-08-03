"""
Demo script for DSA Solo Leveling

This script demonstrates the key features of the application
without requiring the full GUI to run.
"""

import json
import os
from models.data_models import JSONDataLoader, PlayerStats, ProgressTracker, QuestStatus


def demo_data_loading():
    """Demonstrate data loading functionality"""
    print("🔄 Data Loading Demo")
    print("=" * 40)
    
    # Check if data file exists
    data_file = "../dsa_queastions.json"
    if not os.path.exists(data_file):
        data_file = "dsa_queastions.json"
    
    if not os.path.exists(data_file):
        print("❌ DSA questions file not found")
        return []
    
    # Load data
    loader = JSONDataLoader(data_file)
    steps = loader.load_data()
    
    print(f"📚 Loaded {len(steps)} learning steps")
    
    # Display summary
    total_topics = 0
    for i, step in enumerate(steps[:3]):  # Show first 3 steps
        print(f"\n{i+1}. {step.step_title}")
        print(f"   📖 Sub-steps: {len(step.sub_steps)}")
        print(f"   📝 Topics: {step.total_topics}")
        total_topics += step.total_topics
        
        # Show first sub-step details
        if step.sub_steps:
            sub_step = step.sub_steps[0]
            print(f"   🔹 First sub-step: {sub_step.sub_step_title}")
            if sub_step.topics:
                print(f"      Example topic: {sub_step.topics[0].question_title}")
    
    if len(steps) > 3:
        remaining_topics = sum(step.total_topics for step in steps[3:])
        print(f"\n... and {len(steps) - 3} more steps with {remaining_topics} topics")
    
    print(f"\n📊 Total Topics Available: {total_topics}")
    return steps


def demo_progress_tracking():
    """Demonstrate progress tracking functionality"""
    print("\n🎯 Progress Tracking Demo")
    print("=" * 40)
    
    # Create progress tracker
    tracker = ProgressTracker()
    
    # Simulate some progress
    sample_topics = ["topic1", "topic2", "topic3", "topic4", "topic5"]
    
    print("📝 Simulating topic completion...")
    for i, topic_id in enumerate(sample_topics):
        if i < 3:
            status = QuestStatus.COMPLETED
        elif i < 4:
            status = QuestStatus.IN_PROGRESS
        else:
            status = QuestStatus.AVAILABLE
        
        tracker.update_topic_status(topic_id, status)
        print(f"   {topic_id}: {status.value}")
    
    # Show progress data
    print(f"\n💾 Progress data: {tracker.progress_data}")
    
    return tracker


def demo_player_stats():
    """Demonstrate player statistics functionality"""
    print("\n🏆 Player Stats Demo")
    print("=" * 40)
    
    # Create player stats
    player = PlayerStats()
    
    print(f"🎮 Starting Stats:")
    print(f"   Level: {player.level}")
    print(f"   Rank: {player.rank}")
    print(f"   Experience: {player.experience}")
    print(f"   Completed: {player.total_completed}")
    
    # Simulate gaining experience
    print(f"\n⚡ Gaining experience from completing topics...")
    
    # Complete some easy topics
    for i in range(3):
        player.gain_experience(15)  # Easy topic XP
        player.total_completed += 1
        print(f"   Completed topic {i+1}: +15 XP")
    
    # Complete some medium topics
    for i in range(2):
        player.gain_experience(25)  # Medium topic XP
        player.total_completed += 1
        print(f"   Completed medium topic {i+1}: +25 XP")
    
    # Complete a hard topic
    player.gain_experience(40)  # Hard topic XP
    player.total_completed += 1
    print(f"   Completed hard topic: +40 XP")
    
    print(f"\n🎯 Final Stats:")
    print(f"   Level: {player.level}")
    print(f"   Rank: {player.rank}")
    print(f"   Experience: {player.experience}")
    print(f"   Completed: {player.total_completed}")
    
    return player


def demo_ranking_system():
    """Demonstrate the ranking system"""
    print("\n🏅 Ranking System Demo")
    print("=" * 40)
    
    # Create player and simulate progression
    player = PlayerStats()
    
    rank_requirements = [
        (0, "E-Rank Hunter"),
        (10, "D-Rank Hunter"), 
        (20, "C-Rank Hunter"),
        (30, "B-Rank Hunter"),
        (40, "A-Rank Hunter"),
        (50, "S-Rank Hunter")
    ]
    
    print("🎖️ Rank Progression:")
    for level_req, rank_name in rank_requirements:
        print(f"   Level {level_req:2d}+: {rank_name}")
    
    # Simulate rapid progression
    print(f"\n🚀 Simulating progression...")
    print(f"Starting: Level {player.level} - {player.rank}")
    
    # Gain enough XP to reach different levels
    target_levels = [5, 15, 25, 35, 45, 55]
    
    for target in target_levels:
        while player.level < target:
            player.gain_experience(100)  # Big XP boost for demo
        
        print(f"Reached: Level {player.level} - {player.rank}")


def main():
    """Main demo function"""
    print("🎮 DSA Solo Leveling - Feature Demo")
    print("=" * 50)
    
    try:
        # Run demos
        steps = demo_data_loading()
        tracker = demo_progress_tracking()
        player = demo_player_stats()
        demo_ranking_system()
        
        print("\n✅ Demo completed successfully!")
        print("🚀 Ready to run the full application with: python main.py")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()