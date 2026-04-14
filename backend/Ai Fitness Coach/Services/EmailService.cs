using System.Net;
using System.Net.Mail;
namespace Ai_Fitness_Coach.Services
{
    public class EmailService : IEmailService
    {
        private readonly IConfiguration _config;
        public EmailService(IConfiguration config)
        {
            _config = config;
        }
        public async Task SendOtpEmailAsync(string toEmail, string otp)
        {
            var fromEmail = _config["Email:Username"];
            var password = _config["Email:Password"];
            var smtpClient = new SmtpClient("smtp.gmail.com")
            {
                Port = 587,
                Credentials = new NetworkCredential(fromEmail, password),
                EnableSsl = true
            };
            var mail = new MailMessage
            {
                From = new MailAddress(fromEmail),
                Subject = "elFa7l eltare5y Sh3bola sent your OTP code.",
                Body = $"Your verification code is: {otp}",
                IsBodyHtml = false
            };
            mail.To.Add(toEmail);

            await smtpClient.SendMailAsync(mail);
        }
    }
}
