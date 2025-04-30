{{- define "bull-signal-bot.name" -}}
bull-signal-bot
{{- end }}

{{- define "bull-signal-bot.fullname" -}}
{{ .Release.Name }}-bull-signal-bot
{{- end }}
