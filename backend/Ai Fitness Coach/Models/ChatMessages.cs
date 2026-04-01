using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
namespace Ai_Fitness_Coach.Models
{
    public class ChatMessage
    {
        [Key]
        public int Id { get; set; }
        [Required]
        public int SessionId { get; set; }
        [ForeignKey("SessionId")]
        public ChatSession ChatSession { get; set; } = null!;
        [Required]
        [MaxLength(100)]
        public string Sender { get; set; }=string.Empty;
        [Required]
        public string Message { get; set; }= string.Empty;
        public DateTime SentAt { get; set; } = DateTime.UtcNow;
    }
}