export default async function handler(req, res) {
    // 1. Only allow POST requests
    if (req.method !== 'POST') {
        return res.status(405).json({ message: 'Method Not Allowed' });
    }

    try {
        const { name, email, subject, message } = req.body;

        // 2. Reference the NAME of the variable, NOT the URL itself
        // You will paste the actual URL into the Vercel Dashboard later
        const webhookURL = process.env.DISCORD_WEBHOOK_URL;

        if (!webhookURL) {
            return res.status(500).json({ message: 'Webhook configuration missing' });
        }

        const discordPayload = {
            content: "🚀 **New Portfolio Contact**",
            embeds: [{
                title: subject || "No Subject",
                color: 5814783, 
                fields: [
                    { name: "Sender", value: name || "Anonymous", inline: true },
                    { name: "Email", value: email || "Not Provided", inline: true },
                    { name: "Message", value: message || "No message content." }
                ],
                timestamp: new Date().toISOString()
            }]
        };

        const response = await fetch(webhookURL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(discordPayload)
        });

        if (response.ok) {
            return res.status(200).json({ message: 'Transmission Successful' });
        } else {
            return res.status(500).json({ message: 'Failed to send to Discord' });
        }
    } catch (error) {
        return res.status(500).json({ message: 'Internal Server Error', error: error.message });
    }
}