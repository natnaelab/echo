document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', () => {
            document.querySelector('.mobile-menu')?.classList.toggle('hidden');
        });
    }

    if (typeof feather !== 'undefined') {
        feather.replace();
    }

    setupChatFeatures();
    scrollToBottom();
});

function setupChatFeatures() {
    const showMembersBtn = document.getElementById('show-members');
    const onlineUsersSidebar = document.getElementById('online-users-sidebar');

    if (showMembersBtn && onlineUsersSidebar) {
        showMembersBtn.addEventListener('click', () => {
            onlineUsersSidebar.classList.toggle('hidden');
        });
    }

    const messageForm = document.getElementById("message-form");
    if (!messageForm) return;

    const messageInput = messageForm.querySelector("textarea");
    if (!messageInput) return;

    messageInput.addEventListener("input", function() {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + "px";
    });

    messageInput.addEventListener("keydown", function(e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            if (this.value.trim()) {
                htmx.trigger(messageForm, "submit");
            }
        }
    });

    messageForm.addEventListener("htmx:wsAfterSend", () => {
        messageInput.value = '';
        messageInput.style.height = "auto";
    });
}

document.body.addEventListener("htmx:wsBeforeSend", (evt) => {
    if (evt.detail.elt.id === 'message-form') {
        const messageInput = evt.detail.elt.querySelector('textarea');
        if (!messageInput?.value.trim()) {
            evt.preventDefault();
        }
    }
});

document.body.addEventListener('htmx:wsAfterMessage', scrollToBottom);

function scrollToBottom() {
    const container = document.getElementById("messages-container");
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}
