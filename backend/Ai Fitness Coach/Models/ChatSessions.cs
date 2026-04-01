using Ai_Fitness_Coach.Models;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
namespace Ai_Fitness_Coach.Models
{
    public class ChatSession
    {
        [Key]
        public int Id { get; set; }
        [Required]
        public int UserId { get; set; }
        [ForeignKey("UserId")]
        public User User { get; set; } = null!;
        public DateTime StartedAt { get; set; } = DateTime.UtcNow;
        public ICollection<ChatMessage> ChatMessages { get; set; }=new List<ChatMessage>();
    }
}